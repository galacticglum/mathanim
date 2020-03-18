from typing import Union, List
from mathanim.actions import Action

class Sequence:
    '''
    A sequence is a chain of actions (and/or other sequences), executed one after the other, used to build animations.

    '''

    def __init__(self, *sequence_items: List[Action]):
        '''
        Initializes the sequence.

        :param *sequence_items:
            An optional list of nested sequence items.
        
        '''

        self.sequence_items = sequence_items

    def get_value(self, time):
        '''
        Gets the value of the sequence at the specified time.

        :param time:
            The time, given as a :class:`mathanim.Timecode`, relative to the start of the sequence.
        :returns:
            The value of the sequence after the specified time.

        '''

        # actionA[0-3],actionB[4,6])...
        pass

    @property
    def duration(self):
        '''
        Gets the total duration of the sequence.

        '''

        return sum(item.duration for item in self.sequence_items)

# A sequence item is any item that can be added to a sequence.
SequenceItem = Union[Action, Sequence]

def chain(*sequence_items: List[SequenceItem]) -> Sequence:
    '''
    Chains a list of sequence items together so that they occur sequentially.

    :note:
        An action may also be passed into method and the chaining will still work.
        This is because an action is considered a sequence.

    :param *sequence_items:
        The sequence items to chain.
    :returns:
        A sequence consisting of the items in the order of the input.

    '''

    return Sequence(sequence_items)

def combine(*sequence_items: List[SequenceItem]) -> Sequence:
    '''
    Combines a list of sequence items together so that they occur in parallel.

    '''

    pass