from typing import Literal

from application.model.action.action import Action
from application.model.action.action_set import ActionSet


class ActivateAirLoopActionSet(ActionSet):

    def __init__(self,
                 location: Literal['compost_loop', 'shredder_storage', 'bioreactor1', 'bioreactor2', 'bsf_reproduction',
                                   'sieve'] = 'compost_loop',
                 ):

        location_mapping = {
            'compost_loop': '0',
            'shredder_storage': '1',
            'bioreactor1': '2',
            'bioreactor2': '3',
            'bsf_reproduction': '4',
            'sieve': '5'
        }
        value = location_mapping.get(location)

        super().__init__(iterable=[
            Action('e1', value),
            Action('e0', value)
        ])
