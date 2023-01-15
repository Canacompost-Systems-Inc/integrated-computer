from typing import Literal

from application.model.action.action import Action
from application.model.action.action_set import ActionSet


class SetRotaryValveCompostLoopActionSet(ActionSet):

    def __init__(self,
                 location: Literal['air_loop', 'shredder_storage', 'bioreactor1', 'bioreactor2', 'bsf_reproduction',
                                   'sieve'] = 'air_loop',
                 ):

        # Open: 2
        location_mapping = {
            'air_loop': '0',
            'shredder_storage': '5',
            'bioreactor1': '3',
            'bioreactor2': '2',
            'bsf_reproduction': '4',
            'sieve': '',
        }
        value = location_mapping.get(location)

        super().__init__(iterable=[
            Action('e2', value)
        ])
