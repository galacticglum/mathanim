from abc import ABC, abstractmethod

class Action(ABC):
    '''
    The base Action class.
    
    '''

    def __init__(self, duration):
        '''
        Initializes an Action.

        :param duration:
            The duration, given as a Timecode, of the Action.

        '''

        self.duration = duration

    @abstractmethod
    def get_value(self, time):
        '''
        Gets the value of the Action at the specified time.

        :param time:
            The time, given as a Timecode, relative to the start of the Action (0).
        :returns:
            The value of the Action after the specified time.

        '''

        pass

class Ramp(Action):
    '''
    Interpolates from an initial value to a destination value.

    '''

    @staticmethod
    def linear(a, b, t):
        return a + (b - a) * t

    def __init__(self, initial_value, destination_value, duration, func=None):
        '''
        Initializes a Ramp.

        :param initial_value:
            The initial value of the ramp.
        :param destination_value:
            The final value of the ramp.
        :param duration:
            The duration of the ramp, given as a Timecode.
        :param func:
            The ramp function; takes in an initial value, destination value, and time. Defaults to linear.
        '''

        self.initial_value = initial_value
        self.destination_value = destination_value
        self.func = func if func is not None else Ramp.linear

        super().__init__(duration)

    def get_value(self, time):
        t = time / self.duration
        return self.func(self.initial_value, self.destination_value, t)