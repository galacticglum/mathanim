from colour import Color
from numbers import Number
from mathanim.utils import Vector2
from abc import ABC, abstractmethod
from mathanim.errors import ArgumentError
from mathanim.sequences import SequenceItem

class Action(SequenceItem):
    '''
    The base action class.
    
    '''

    def __init__(self, duration):
        '''
        Initializes an instance of :class:`Action`.

        :param duration:
            The duration of the action, in seconds.

        '''

        self._duration = duration

    @property
    def duration(self):
        '''
        Gets the duration of this action.
        
        '''
        
        return self._duration

class Ramp(Action):
    '''
    Interpolates from an initial value to a destination value.

    '''

    @staticmethod
    def linear(a, b, t):
        return a + (b - a) * t

    def __init__(self, initial_value, destination_value, duration, func=None, map_func=None):
        '''
        Initializes an instance of :class:`Ramp`.

        :param initial_value:
            The initial value of the ramp.
        :param destination_value:
            The final value of the ramp.
        :param duration:
            The duration of the ramp, in seconds.
        :param func:
            The ramp interpolation function; takes in an initial value, destination value, and time.
            Defaults to linear.

            This function should operate on a single value. For example, if the initial and destination
            values of the ramp is a tuple, list, vectors, colours, etc..., the ramp will automatically
            apply the interpolation function to each component of the value. This behaviour can be
            overwritten using the ``map_func`` parameter.
        :param map_func:
            A function that specifies how the initial and destination values should be mapped to the
            interpolation function. If set to ``None``, the default behaviour will be applied.

        '''

        self.__initial_value = initial_value
        self.__destination_value = destination_value
        self._check_values()

        self.func = func or Ramp.linear
        self.map_func = map_func or Ramp._default_map_func 

        super().__init__(duration)

    @property
    def initial_value(self):
        '''
        Gets the initial value of the ramp.

        '''

        return self.__initial_value

    @initial_value.setter
    def initial_value(self, value):
        '''
        Sets the initial value of the ramp.
    
        '''

        self.__initial_value = value
        self._check_values()

    @property
    def destination_value(self):
        '''
        Gets the destination value of the ramp.

        '''

        return self.__destination_value

    @destination_value.setter
    def destination_value(self, value):
        '''
        Sets the destination value of the ramp.
    
        '''

        self.__destination_value = value
        self._check_values()

    def _check_values(self):
        '''
        Checks the initial and destination values of the ramp.

        '''

        are_numbers = isinstance(self.initial_value, Number) and isinstance(self.destination_value, Number)
        if not are_numbers and type(self.initial_value) != type(self.destination_value):
            raise TypeError('Ramp action got mismatched initial and destination value types ({} != {})'
                .format(self.initial_value.__class__.__name__, self.destination_value.__class__.__name__))

        if isinstance(self.initial_value, tuple) or isinstance(self.initial_value, list):
            if len(self.initial_value) != len(self.destination_value):
                raise ArgumentError('Ramp action got iterables of mismatched lengths.')

    @staticmethod
    def _default_map_func(ramp, t):
        '''
        The default mapping function.

        :param ramp:
            An instance of the :class:`Ramp` action.
        :param t:
            The time (alpha) parameter of the interpolation function.
            It is a value from 0 to 1 indicating the percent complete.
        :returns:
            An object of the same type as the ramp's initial and destination
            value representing the interpolated value at the specified time.

        '''

        is_tuple = isinstance(ramp.initial_value, tuple)
        if is_tuple or isinstance(ramp.initial_value, list):
            n_components = len(ramp.initial_value)
            value = [0] * n_components
            for i in range(n_components):
                value[i] = ramp.func(ramp.initial_value[i], ramp.destination_value[i], t)

            # Convert back to tuple if the original value was a tuple.
            if is_tuple:
                value = tuple(value)
        elif isinstance(ramp.initial_value, Vector2):
            value = Vector2(
                ramp.func(ramp.initial_value.x, ramp.destination_value.x, t),
                ramp.func(ramp.initial_value.y, ramp.destination_value.y, t)
            )
        elif isinstance(ramp.initial_value, Color):
            value = Color(
                red=ramp.func(ramp.initial_value.red, ramp.destination_value.red, t),
                green=ramp.func(ramp.initial_value.green, ramp.destination_value.green, t),
                blue=ramp.func(ramp.initial_value.blue, ramp.destination_value.blue, t)
            )
        else:
            value = ramp.func(ramp.initial_value, ramp.destination_value, t)
            
        return value

    def get_value(self, time):
        '''
        Gets the value of the ramp at the specified time.

        :param time:
            The time, in seconds, relative to the start of the action.
        :returns:
            The value of the ramp at the specified time. 
            If the time exceeds the duration of the sequence, None is returned.

        '''

        if time > self.duration: return None

        t = time / self.duration
        return self.map_func(self, t)

class Procedure(Action):
    '''
    General-purpose action that uses a custom function
    
    '''

    def __init__(self, duration, func, *func_args):
        '''
        Initializes an instance of :class:`Procedure`.

        :param duration:
            The duration of the procedure, in seconds.
        :param func:
            The custom function to execute.
        :param *func_args:
            Arguments to the procedure function.

        '''

        self.func = func
        self.func_args = func_args
        super().__init__(duration)

    def get_value(self, time):
        '''
        Gets the value of the procedure at the specified time.

       :param time:
            The time, in seconds, relative to the start of the action.
        :returns:
            The value of the ramp at the specified time.

        '''

        return self.func(time, *self.func_args)