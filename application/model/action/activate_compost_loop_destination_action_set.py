from typing import Literal

from application.model.action.action import Action
from application.model.action.action_set import ActionSet


class ActivateCompostLoopDestinationActionSet(ActionSet):

    def __init__(self,
                 location: Literal['air_loop', 'shredder_storage', 'bioreactor1', 'bioreactor2', 'bsf_reproduction',
                                   'sieve'] = 'air_loop',
                 ):

        # Open: 0
        location_mapping_e1 = {
            'air_loop': '1',
            'shredder_storage': '2',
            'bioreactor1': '4',
            'bioreactor2': '5',
            'bsf_reproduction': '3',
            'sieve': ''
        }
        # Open: 3
        location_mapping_e2 = {
            'air_loop': '0',
            'shredder_storage': '5',
            'bioreactor1': '3',
            'bioreactor2': '2',
            'bsf_reproduction': '4',
            'sieve': '',
        }
        value_e2 = location_mapping_e2.get(location)
        value_e1 = location_mapping_e1.get(location)

        super().__init__(iterable=[
            Action('e2', value_e2),
            Action('e1', value_e1)
        ])
