from typing import Literal

from application.model.action.action import Action
from application.model.action.action_set import ActionSet


class SetRotaryValveFromAirLoopActionSet(ActionSet):

    def __init__(self,
                 location: Literal['compost_loop', 'shredder_storage', 'bioreactor1', 'bioreactor2', 'bsf_reproduction',
                                   'sieve'] = 'compost_loop',
                 ):

        # Open: 2
        location_mapping = {
            'compost_loop': '0',
            'shredder_storage': '3',
            'bioreactor1': '1',
            'bioreactor2': '4',
            'bsf_reproduction': '5',
            'sieve': '0',
        }
        value = location_mapping.get(location)

        super().__init__(iterable=[
            Action('e0', value)
        ])
