import copy
from intervaltree import IntervalTree
from mathanim.utils import rgetattr, rsetattr

class Timecode:
    def __init__(self, hours=0, minutes=0, seconds=0, frames=0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.frames = frames

    def total_frames(self, fps):
        return self.frames + fps * (self.seconds + self.minutes * 60 + self.hours * 3600)
    
    def __add__(self, other):
        return Timecode(
            hours=self.hours + other.hours,
            minutes=self.minutes + other.minutes,
            seconds=self.seconds + other.seconds,
            frames=self.frames + other.frames
        )

    def __sub__(self, other):
        return Timecode(
            hours=self.hours - other.hours,
            minutes=self.minutes - other.minutes,
            seconds=self.seconds - other.seconds,
            frames=self.frames - other.frames
        )

    def __mul__(self, other):
        return Timecode(
            hours=self.hours * other.hours,
            minutes=self.minutes * other.minutes,
            seconds=self.seconds * other.seconds,
            frames=self.frames * other.frames
        )

    def __div__(self, other):
        return Timecode(
            hours=self.hours / other.hours,
            minutes=self.minutes / other.minutes,
            seconds=self.seconds / other.seconds,
            frames=self.frames / other.frames
        )

class Animation:
    '''
    A wrapper around scene objects and sequences. An animation is associated with an instance of a
    scene object and each sequence in the animation modifies the object in some way (i.e. with a
    sequence item bound to an attribute).

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
            The object to animate.
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
            A copy of the object with the animation at the specified time applied.

        '''

        animation_object = copy.deepcopy(self.initial_object)
        for instance in self.sequence_instances:
            value = instance.sequence_item.get_value(time)
            if instance.map_func is not None:
                attribute_value = rgetattr(animation_object, instance.name)
                value = instance.map_func(attribute_value, value)
            
            rsetattr(animation_object, instance.name, value)
        
        return animation_object

class Timeline:
    '''
    A collection of animations that is simulated frame by frame.
    
    '''
    
    def __init__(self, fps):
        '''
        Initializes an instance of :class:`Timeline`.

        :param fps:
            The frames per second of the timeline.

        '''

        self.fps = fps
        self._animation_tree = IntervalTree()

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

        start_frame = self._animation_tree.end() + padding * self.fps
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
            start_frame *= self.fps

        for animation in animations:
            # The interval tree library does not include the upper bound so we need to add a frame
            # to the upper bound. The actual end frame of the animation is end_frame - 1.
            end_frame = start_frame + round(animation.duration * self.fps)
            self._animation_tree[start_frame:end_frame] = animation

    def get(self, frame):
        '''
        Getts the timeline at the specified frame.

        :returns:
            A list of objects comprising the frame.

        '''

        objects = []
        for interval in self._animation_tree[frame]:
            # Calculate the time by finding the percent completion of the animation
            #
            # We subtract one in the denominator since interval.end is actually offset by a single frame.
            # This is due to the fact that the interval tree implementation excludes the upper bound.
            t = (frame - interval.begin) / (interval.end - interval.begin - 1)
            objects.append(interval.data.animate(interval.data.duration * t))

        return objects

    @property
    def total_frames(self):
        '''
        Gets the duration of this timeline, in frames.

        '''

        return self._animation_tree.end() - 1
    
    @property
    def total_seconds(self):
        '''
        Gets the duration of this timeline, in seconds.

        '''

        return self.total_frames / self.fps
        
    def __iter__(self):
        self._current_frame = 0
        return self

    def __next__(self):
        if self._current_frame > self.total_frames:
            raise StopIteration
        
        objects = self.get(self._current_frame)
        self._current_frame += 1
        return objects
