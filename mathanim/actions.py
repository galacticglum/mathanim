from typing import Callable, Union
from abc import ABC, abstractmethod

from mathanim.timeline import Timecode
Number = Union[int, float]

class Action(ABC):
    '''
    The base action class.
    
    '''

    def __init__(self, duration: Timecode):
        '''
        Initializes an action.

        :param duration:
            The duration, given as a :class:`mathanim.Timecode`, of the action.

        '''

        self.duration = duration

    @abstractmethod
    def get_value(self, time: Timecode):
        '''
        Gets the value of the action at the specified time.

        :param time:
            The time, given as a :class:`mathanim.Timecode`, relative to the start of the action.
        :returns:
            The value of the action after the specified time.

        '''

        pass

class Ramp(Action):
    '''
    Interpolates from an initial value to a destination value.

    '''

    @staticmethod
    def linear(a: Number, b: Number, t: Number) -> Number:
        return a + (b - a) * t

    def __init__(self, initial_value: float, destination_value: Number, 
                 duration: Timecode, func: Callable[[Number, Number], Number] = None):
        '''
        Initializes a ramp.

        :param initial_value:
            The initial value of the ramp.
        :param destination_value:
            The final value of the ramp.
        :param duration:
            The duration of the ramp, given as a :class:`mathanim.Timecode`.
        :param func:
            The ramp interpolation function; takes in an initial value, destination value, and time. Defaults to linear.
        '''

        self.initial_value = initial_value
        self.destination_value = destination_value
        self.func = func if func is not None else Ramp.linear

        super().__init__(duration)

    def get_value(self, time: Timecode):
        t = time / self.duration
        return self.func(self.initial_value, self.destination_value, t)