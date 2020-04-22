import cv2
import tqdm
import copy
import cairo
import numpy as np
from colour import Color
from pathlib import Path
from mathanim.errors import PathError
from intervaltree import IntervalTree
from mathanim.objects import SceneObject
from mathanim.utils import rgetattr, rsetattr, convert_colour, BidirectionalMap

class Animation:
    '''
    A wrapper around scene objects and sequences. An animation is associated with an instance of a
    :class:`mathanim.objects.SceneObject` and each sequence in the animation modifies the object in 
    some way (i.e. with a sequence item bound to an attribute).

    '''

    class SequenceInstance:
        '''
        A sequence item that is binded to an attribute for use in an :class:`Animation`.

        :note:
            This acts like a new sequence that takes in an object as its input and applies 
            the specified sequence item on the specified attribute of the input object.

        '''

        def __init__(self, sequence_item, name, map_func=None):
            '''
            Initializes an instance of :class:`Animation.SequenceInstance`.

            :param sequence_item:
                The :class:`SequenceItem` to bind to the attribute. 
            :param name:
                The name of the attribute to bind the sequence to. This supports "dot" notation
                (i.e. ``foo.bar.baz``).
            :param map_func:
                A custom mapping function specifying how the animated value should be applied 
                to the attribute. This function takes in the attribute and the output value of
                the sequence item as inputs and returns the modified attribute value.            

            '''

            self.sequence_item = sequence_item
            self.name = name
            self.map_func = map_func

    def __init__(self, animation_object, *sequence_instances):
        '''
        Initializes an instance of :class:`Animation`.

        :param animation_object:
            The :class:`mathanim.objects.SceneObject` to animate.
        :param *sequence_instances:
            The sequence instances to add to the animation. This can either be an 
            :class:`Animation.SequenceInstance` object or a dictionary mapping 
            attribute names to their bounded sequence items.

        '''

        self.initial_object = animation_object
        self.sequence_instances = []

        for sequence_instance in sequence_instances:
            if isinstance(sequence_instance, dict):
                for name in sequence_instance:
                    self.sequence_instances.append(Animation.SequenceInstance(sequence_instance[name], name))
            elif isinstance(sequence_instance, Animation.SequenceInstance):
                self.sequence_instances.append(sequence_instance)
            else:
                raise TypeError('Invalid sequence instance argument specified. Expected dictionary or object ' +
                                'of type Animation.SequenceInstance but found {} instead'.format(type(sequence_instance)))
         
    @property
    def duration(self):
        '''
        Gets the duration of this animation.

        :note:
            This is the maximum duration of all items in the sequence.
        
        :returns:
            The duration of this animation, in seconds.

        '''
        
        return max(instance.sequence_item.duration for instance in self.sequence_instances)

    def animate(self, time):
        '''
        Animate this :class:`Animation`.

        :param time:
            The time relative to the start of the sequence, in seconds.
        :returns:
            A copy of the :class:`mathanim.objects.SceneObject` with the animation 
            at the specified time applied.

        '''

        animation_object = copy.deepcopy(self.initial_object)
        for instance in self.sequence_instances:
            value = instance.sequence_item.get_value(time)
            if instance.map_func is not None:
                attribute_value = rgetattr(animation_object, instance.name)
                value = instance.map_func(attribute_value, value)
            
            if value is None: continue
            rsetattr(animation_object, instance.name, value)
        
        return animation_object

class FrameSnapshot:
    '''
    A snapshot of a single frame in the timeline.

    '''
    
    def __init__(self, frame, objects):
        '''
        Initializes an instance of :class:`FrameSnapshot`.

        :param frame:
            The frame that this snapshot was taken.
        :param objects:
            The objects in this frame.

        '''

        self.frame = frame
        self.objects = objects

class SceneSettings:
    '''
    The settings of a Scene.

    '''
    
    def __init__(self, reference_width, reference_height, fps):
        '''
        Initializes an instance of :class:`SceneSettings`.

        :param width:
            The width of the scene's reference frame.
        :param height:
            The height of the scene's reference frame.
        :param fps:
            The frames per second of the scene.
        
        '''

        self.reference_width = reference_width
        self.reference_height = reference_height
        self.fps = fps

# HDTV (1080p at 30 frames per second) scene preset.
SceneSettings.HDTV30 = SceneSettings(1920, 1080, 30)

# HDTV (1080p at 60 frames per second) scene preset.
SceneSettings.HDTV60 = SceneSettings(1920, 1080, 60)

class Scene:
    def __init__(self, settings=SceneSettings.HDTV60, background_colour='black'):
        '''
        Initializes an instance of :class:`Scene`.

        :param settings:
            The :class:`SceneSettings` to use with this scene.
            Defaults to 1080p at 60 fps (HDTV).
        :param background_colour:
            The background colour of the scene. Defaults to black.

        '''

        self.settings = settings
        self.background_colour = convert_colour(background_colour)

        self._animation_tree = IntervalTree()
        # Maps objects to a unique identifier
        self._object_ids = {}

    def add(self, *animations, padding=0):
        '''
        Appends the animations to the end of the timeline (i.e. directly after the last animation).

        :note:
            If multiple animations are given, they will be placed in parallel.
            This will place all of the animations starting at the same time.

        :param *animations:
            The :class:`Animation` objects to add.
        :param padding:
            The amount of time, in seconds, to pad between the end of the timeline and the new animations. 

        '''

        start_frame = self._animation_tree.end() + padding * self.settings.fps
        self.add_at(start_frame, *animations, seconds=False)

    def add_at(self, time, *animations, seconds=True):
        '''
        Places the animations onto the timeline at the specified time.

        :note:
            If multiple animations are given, they will be placed in parallel.
            This will place all of the animations starting at the same time.

        :param time:
            The time, in seconds, where the animations should be placed.
        :param *animations:
            The :class:`Animation` objects to place.
        :param seconds:
            Indicates whether the time is given in seconds or frames. If ``True``, the time is in seconds;
            otherwise, it is in frames. Defaults to ``True.

        '''

        start_frame = time
        if seconds:
            start_frame *= self.settings.fps

        for animation in animations:
            # The interval tree library does not include the upper bound so we need to add a frame
            # to the upper bound. The actual end frame of the animation is end_frame - 1.
            end_frame = start_frame + round(animation.duration * self.settings.fps)
            self._animation_tree[start_frame:end_frame] = animation
        
    @property
    def snapshots(self):
        '''
        Gets all the frame snapshots in this timeline.

        '''

        for frame in range(self.total_frames):
            objects = []
            for interval in self._animation_tree[frame]:
                # Calculate the time by finding the percent completion of the animation
                #
                # We subtract one in the denominator since interval.end is actually offset by a single frame.
                # This is due to the fact that the interval tree implementation excludes the upper bound.
                t = (frame - interval.begin) / (interval.end - interval.begin - 1)
                objects.append(interval.data.animate(interval.data.duration * t))

            yield FrameSnapshot(frame, objects)

    @property
    def total_frames(self):
        '''
        Gets the duration of this timeline, in frames.

        '''

        return self._animation_tree.end()
    
    @property
    def total_seconds(self):
        '''
        Gets the duration of this timeline, in seconds.

        '''

        return self.total_frames / self.settings.fps

    @property
    def background_colour(self):
        '''
        The background colour of the scene.

        '''

        return self.__background_colour
    
    @background_colour.setter
    def background_colour(self, value):
        '''
        Sets the background colour of the scene.

        '''

        self.__background_colour = convert_colour(value)

    def __enter__(self):
        print('scene entered')
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print('scene exited')

    def _clear(self, render_context):
        '''
        Clear the screen.

        '''

        render_context.set_source_rgb(*self.background_colour.rgb)
        render_context.paint()

    def export(self, filepath, output_width=None, output_height=None,
               show_progress_bar=True, overwrite=True, codec='mp4v'):
        '''
        Export the scene to a video file.

        :param filepath:
            The path where the rendered result should be saved.
        :param output_width:
            The horizontal resolution of the video, in pixels.
            Defaults to the width of the reference frame.
        :param output_height:
            The vertical resolution of the video, in pixels.
            Defaults to the height of the reference frame.
        :param show_progress_bar:
            Indicates whether a progress bar should be displayed while the video is rendered.
            Defaults to ``True``.
        :param overwrite:
            Indicates whether the export file should be overwritten in the case that it exists.
            Defaults to ``True``.
        :param codec:
            The FourCC indicating the codec of the exported video. Defaults to mp4v encoding.
            For a full list of video encoding codes, see https://www.fourcc.org/codecs.php.

        '''

        if output_width is None:
            output_width = self.settings.reference_width

        if output_height is None:
            output_height = self.settings.reference_height

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, output_width, output_height)
        context = cairo.Context(surface)

        # Normalize coordinate system to the reference frame
        context.scale(output_width / self.settings.reference_width, output_height / self.settings.reference_height)

        filepath = Path(filepath)
        if filepath.exists():
            if not filepath.is_file():
                raise PathError('Tried to export scene to file but \'{}\' is not a valid filepath.'.format(filepath))

            if not overwrite:
                raise IOError('The file \'{}\' already exists and overwrite is disabled!'.format(filepath))

            filepath.unlink()
            
        filepath.parent.mkdir(parents=True, exist_ok=True)

        output_shape = (output_width, output_height)
        video = cv2.VideoWriter(str(filepath), cv2.VideoWriter_fourcc(*codec), self.settings.fps, output_shape)
        for snapshot in tqdm.tqdm(self.snapshots, disable=not show_progress_bar):
            self._clear(context)
            for frame_object in snapshot.objects:
                # Isolate transformations using save/restore.
                context.save()
                frame_object.draw(context)
                context.restore()
    
            data = np.ndarray(shape=(*reversed(output_shape), 4), dtype=np.uint8, buffer=surface.get_data())

            # Drop alpha values from frame data
            data = data[:,:,:3]
            video.write(data)

        video.release()