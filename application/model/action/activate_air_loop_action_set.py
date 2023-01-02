from typing import Literal

from application.model.action.action import Action
from application.model.action.action_set import ActionSet


class ActivateAirLoopActionSet(ActionSet):

    def __init__(self,
                 location: Literal['compost_loop', 'shredder_storage', 'bioreactor1', 'bioreactor2', 'bsf_reproduction',
                                   'sieve'] = 'compost_loop',
                 ):

        # TODO - updated based on hardware, need to see if this is permanent
        # Open: 2
        location_mapping_e0 = {
            'compost_loop': '4',
            'shredder_storage': '3',
            'bioreactor1': '1',
            'bioreactor2': '0',
            'bsf_reproduction': '5',
            'sieve': ''
        }
        # Open: 0
        location_mapping_e1 = {
            'compost_loop': '3',
            'shredder_storage': '2',
            'bioreactor1': '4',
            'bioreactor2': '5',
            'bsf_reproduction': '1',
            'sieve': ''
        }
        value_e0 = location_mapping_e0.get(location)
        value_e1 = location_mapping_e1.get(location)

        super().__init__(iterable=[
            Action('e1', value_e1),
            Action('e0', value_e0)
        ])
