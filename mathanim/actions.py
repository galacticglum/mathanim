from typing import Callable, Union
from abc import ABC, abstractmethod

Number = Union[int, float]

class Action(ABC):
    '''
    The base action class.
    
    '''

    def __init__(self, duration: Number):
        '''
        Initializes an action.

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

    @abstractmethod
    def get_value(self, time: Number):
        '''
        Gets the value of the action at the specified time.

        :param time:
            The time, in seconds, relative to the start of the action.
        :returns:
            The value of the action at the specified time.

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
                 duration: Number, func: Callable[[Number, Number], Number] = None):
        '''
        Initializes a ramp.

        :param initial_value:
            The initial value of the ramp.
        :param destination_value:
            The final value of the ramp.
        :param duration:
            The duration of the ramp, in seconds.
        :param func:
            The ramp interpolation function; takes in an initial value, destination value, and time. Defaults to linear.
        '''

        self.initial_value = initial_value
        self.destination_value = destination_value
        self.func = func if func is not None else Ramp.linear

        super().__init__(duration)

    def get_value(self, time: Number):
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
        return self.func(self.initial_value, self.destination_value, t)

class Procedure(Action):
    '''
    General-purpose action that uses a custom function
    
    '''

    def __init__(self, duration: Number, func: Callable[[Number], object], *func_args):
        '''
        Initializes a procedure.

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

    def get_value(self, time: Number):
        '''
        Gets the value of the procedure at the specified time.

       :param time:
            The time, in seconds, relative to the start of the action.
        :returns:
            The value of the ramp at the specified time.

        '''

        return self.func(time, *self.func_args)