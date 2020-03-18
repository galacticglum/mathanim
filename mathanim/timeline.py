class Timecode:
    def __init__(self, frames):
        self.frames = frames

class Timeline:
    '''
    A timeline is a collection of sequences that is simulated frame by frame.
    
    '''
    
    def __init__(self):
        self.animations = []

    def add(self, *animations, padding=0):
        '''
        Appends the animations to the end of the timeline (i.e. directly after the last animation).

        :note:
            If multiple animations are given, they will be placed in parallel.
            This will place all of the animations starting at the same time.

        :param *animations:
            The animations, objects of type Animation, to add.
        :param padding:
            the amount of time, given as a Timecode, to pad between the two animations, 

        '''

        pass

    def add_at(self, time, *animations):
        '''
        Places the animations onto the timeline at the specified timecode.

        :note:
            If multiple animations are given, they will be placed in parallel.
            This will place all of the animations starting at the same time.

        :param time:
            The timecode specifying where in the timeline the animations should be placed.
        :param *animations:
            The animations, object of Type Animation, to place.
        '''

        pass