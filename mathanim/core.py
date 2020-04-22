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
from mathanim.utils import rgetattr, rsetattr, convert_colour

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

    def __init__(self, animation_object, *sequence_instances, check_attributes=True):
        '''
        Initializes an instance of :class:`Animation`.

        :param animation_object:
            The :class:`mathanim.objects.SceneObject` to animate.
        :param *sequence_instances:
            The sequence instances to add to the animation. This can either be an 
            :class:`Animation.SequenceInstance` object or a dictionary mapping 
            attribute names to their bounded sequence items.
        :param check_attributes:
            Indicates whether the animation should check if the specified animation object
            has the attributes that the sequences were binded to. Defaults to ``True``.

            Disabling this can be useful if the object's attributes are modified at runtime.

        '''

        self.initial_object = animation_object
        self.sequence_instances = []

        for x in sequence_instances:
            if isinstance(x, dict):
                for name in x:
                    self.sequence_instances.append(Animation.SequenceInstance(x[name], name))
            elif isinstance(x, Animation.SequenceInstance):
                self.sequence_instances.append(x)
            else:
                raise TypeError('Invalid sequence instance argument specified. Expected dictionary or object ' +
                                'of type Animation.SequenceInstance but found {} instead'.format(type(sequence_instance)))

        if not check_attributes: return
        for sequence_instance in self.sequence_instances:
            value = rgetattr(self.initial_object, sequence_instance.name, None)
            if value is None:
                error_message = '{} has no attribute with name \'{}\''.format(self.initial_object.__class__.__name__, sequence_instance.name)
                raise AttributeError(error_message)
         
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

    def animate(self, time, animation_object):
        '''
        Animate this :class:`Animation`.

        :param time:
            The time relative to the start of the sequence, in seconds.
        :param animation_object:
            The object to update with the animated values.
        :returns:
            A copy of the :class:`mathanim.objects.SceneObject` with the animation 
            at the specified time applied.

        '''

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
    
    def __init__(self, reference_width, reference_height):
        '''
        Initializes an instance of :class:`SceneSettings`.

        :param width:
            The width of the scene's reference frame.
        :param height:
            The height of the scene's reference frame.
        
        '''

        self.reference_width = reference_width
        self.reference_height = reference_height

# HDTV (1080p) scene preset.
SceneSettings.HDTV = SceneSettings(1920, 1080)

class Trigger:
    '''
    Triggers are events that are raised at a certain point in time.
    They are added to the timeline to control data flow outside of animation.

    '''

    def __init__(self, time, func, *func_args, frame_delay=0):
        '''
        Initializes an instance of :class:`Trigger`.

        :param time:
            The time, in seconds, that the trigger should be raised.
        :param func:
            The function that should be executed when the trigger is raised.
            
            It has a single parameter: a dictionary of object ids to object values 
            that can be manipulated.
        :param func_args:
            Additional positional arguments that are passed to the execution function.
        :param frame_delay:
            The number of frames to delay the trigger by. Defaults to 0.

        '''

        self.time = time
        self.frame_delay = frame_delay
        self._func = func
        self._func_args = func_args

    def call(self, objects):
        '''
        Raise this trigger.

        '''

        self._func(objects, *self._func_args)

class RemoveTrigger(Trigger):
    '''
    A trigger that removes an object from the timeline.

    '''

    def __init__(self, time, scene_object, frame_delay=0):
        '''
        Initializes an instance of :class:`RemoveTrigger`.

        :param time:
            The time, in seconds, that the object should be removed at.
        :param scene_object:
            The object that should be removed.
        :param frame_delay:
            The number of frames to delay the trigger by. Defaults to 0.

        '''

        super().__init__(time, RemoveTrigger._remove_func, scene_object, frame_delay=frame_delay)

    @staticmethod
    def _remove_func(objects, scene_object):
        '''
        Scene object removal function.

        '''

        object_id = id(scene_object)
        if object_id not in objects: return
        
        del objects[object_id]

class Scene:
    '''
    Represents the screen and all the objects in it.

    '''

    class TimelineItem:
        '''
        An item in the timeline.
        Each item has a start and an end, along with an associated object.
        
        '''

        def __init__(self, start, end, scene_object, animation=None):
            '''
            Initializes an instance of :class:`TimelineItem`.

            :param start:
                The time, in seconds, when the object appears in the scene.
                A value of ``None`` means that this item starts at the beginning of the timeline.
            :param end:
                The time, in seconds, when the object disappears from the scene.
                A value of ``None`` means that this item ends at the end of the timeline.
            :param scene_object:
                The scene object to display.
            :param animation:
                The animation associated with the scene object. Defaults to ``None``.
            
            '''

            self.start = start
            self.end = end
            self.scene_object = scene_object
            self.animation = animation

        @property
        def start(self):
            '''
            The start time of the item, in seconds.

            '''

            return self.__start

        @start.setter
        def start(self, value):
            '''
            Sets the start time of the item, in seconds.
            A value of ``None`` means that this item starts at the beginning of the timeline.

            '''

            self.__start = value if value is not None else 0

        @property
        def duration(self):
            '''
            Gets the duration of this item, in seconds.
            
            :returns:
                The duration, in seconds, or ``None`` if the item has no end time.

            '''

            if self.end is None: return None
            return self.end - self.start

    def __init__(self, settings=SceneSettings.HDTV, background_colour='black'):
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

        self._items = []
        self._triggers = []

    def add(self, *animations, padding=0, remove_animation=False):
        '''
        Appends the animations to the end of the timeline (i.e. directly after the last animation).

        :note:
            If multiple animations are given, they will be placed in parallel.
            This will place all of the animations starting at the same time.

        :param *animations:
            The :class:`Animation` objects to add.
        :param padding:
            The amount of time, in seconds, to pad between the end of the timeline and the new animations. 
        :param remove_animation:
            Indicates whether the animated object should be removed after its animation is complete.
            Defaults to ``False``.

        '''

        self.add_at(self.total_seconds + padding, *animations, remove_animation=remove_animation)

    def add_at(self, time, *animations, remove_animation=False):
        '''
        Places the animations onto the timeline at the specified time.

        :note:
            If multiple animations are given, they will be placed in parallel.
            This will place all of the animations starting at the same time.            

        :param time:
            The time, in seconds, where the animations should be placed.
        :param *animations:
            The :class:`Animation` objects to place.
        :param remove_animation:
            Indicates whether the animated object should be removed after its animation is complete.
            Defaults to ``False``.

        '''

        for animation in animations:
            end_time = time + animation.duration
            if remove_animation:
                # Delay the removal by one frame so that it doesn't remove until the animation is actually done.
                # Since triggers are processed before the frame is returned, if a remove trigger occurs on frame N,
                # it will not appear on frame N...
                self.add_trigger(RemoveTrigger(end_time, animation.initial_object, frame_delay=1))

            self._items.append(Scene.TimelineItem(time, end_time, animation.initial_object, animation))
    
    def add_trigger(self, *triggers):
        '''
        Adds the triggers onto the timeline.

        :param *triggers:
            The :class:`Trigger` objects to place.

        '''

        self._triggers.append(*triggers)

    def render(self, fps):
        '''
        Renders this scene.
        
        :parma fps:
            The frames per second that should be used in rendering.
        :returns:
            Yields each frame in order as a :class:`FrameSnapshot`.

        '''

        total_seconds = self.total_seconds 
        total_frames = round(total_seconds * fps)

        # Build the item tree (these are intervals representing timeline itemss)
        item_tree = IntervalTree()
        for item in self._items:
            start_frame = round(item.start * fps)
            end_frame = round((item.end or total_seconds) * fps)
            item_tree[start_frame:end_frame] = item

        # Map triggers to frames
        triggers = {}
        for trigger in self._triggers:
            frame = round(trigger.time * fps) + trigger.frame_delay
            if frame not in triggers:
                triggers[frame] = []

            triggers[frame].append(trigger)
        
        objects = {}
        for frame in range(total_frames):
            if frame in triggers:
                for trigger in triggers[frame]:
                    trigger.call(objects)

            for interval in item_tree[frame]:
                item = interval.data
                if item.scene_object is None: continue

                scene_object = None
                object_id = id(item.scene_object)
                if object_id not in objects:
                    scene_object = copy.deepcopy(item.scene_object)
                    objects[object_id] = scene_object
                else:
                    scene_object = objects[object_id]

                if item.animation is not None:
                    # Calculate the time by finding the percent completion of the animation
                    #
                    # We subtract one in the denominator since interval.end is actually offset by a single frame.
                    # This is due to the fact that the interval tree implementation excludes the upper bound.
                    t = (frame - interval.begin) / (interval.end - interval.begin - 1)
                    item.animation.animate(interval.data.duration * t, scene_object)

            yield FrameSnapshot(frame, iter(objects.values()))

    @property
    def total_seconds(self):
        '''
        Gets the duration of this scene, in seconds.

        :note:
            If there are many objects in the scene, this can be slow since it
            is a linear, O(n), search on all the items.

        '''
        
        if len(self._items) == 0: return 0

        # The maximum end time is the total duration of the scene.
        # We ignore end times that are None (i.e. they span the entire
        # scene) by treating those as zero.
        return max(self._items, key=lambda x: x.end or 0).end

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
               show_progress_bar=True, overwrite=True, codec='mp4v', fps=60):
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
        :param fps:
            The frames per second of the exported video.

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
        video = cv2.VideoWriter(str(filepath), cv2.VideoWriter_fourcc(*codec), fps, output_shape)
        for snapshot in tqdm.tqdm(self.render(fps), disable=not show_progress_bar):
            self._clear(context)
            for frame_object in snapshot.objects:
                # Isolate transformations using save/restore.
                context.save()
                frame_object.draw(context)
                context.restore()
    
            # Convert image surface buffer to numpy array and drop alpha values from frame data
            data = np.ndarray(shape=(*reversed(output_shape), 4), dtype=np.uint8, buffer=surface.get_data())[:,:,:3]
            video.write(data)

        video.release()