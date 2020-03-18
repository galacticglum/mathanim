from typing import Union, List
from mathanim.actions import Action

# A sequence item is any item that can be added to a sequence.
SequenceItem = Union[Acton, Sequence]

class Sequence:
    '''
    A sequence is a chain of actions (and/or other sequences), executed one after the other, used to build animations.

    '''

    def __init__(*sequenceItems: List[SequenceItem]):
        '''
        Initializes the sequence.

        :param *sequenceItems:
            An optional list of nested sequence items.
        
        '''

        self.sequenceItems = sequenceItems
    
    @property
    def duration(self):
        '''
        Gets the total duration of the sequence.

        '''

        return sum(item.duration for item in self.sequenceItems)

def chain(*sequenceItems: List[SequenceItem]) -> Sequence:
    '''
    Chains a list of sequence items together so that they occur sequentially.

    :note:
        An action may also be passed into method and the chaining will still work.
        This is because an action is considered a sequence.

    :param *sequenceItems:
        The sequence items to chain.
    :returns:
        A sequence consisting of the items in the order of the input.

    '''

    return Sequence(sequenceItems)

def combine(*sequenceItems: List[SequenceItem]) -> Sequence:
    '''
    Combines a list of sequence items together so that they occur in parallel.

    '''

    pass