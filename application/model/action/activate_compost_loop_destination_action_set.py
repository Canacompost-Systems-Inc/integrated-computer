from typing import Literal

from application.model.action.action import Action
from application.model.action.action_set import ActionSet


class ActivateCompostLoopDestinationActionSet(ActionSet):

    def __init__(self,
                 location: Literal['air_loop', 'bioreactor1', 'bioreactor2', 'bsf_reproduction', 'sieve'] = 'air_loop',
                 ):

        location_mapping = {
            'air_loop': '0',
            'bioreactor1': '2',
            'bioreactor2': '3',
            'bsf_reproduction': '4',
            'sieve': '5',
        }
        value = location_mapping.get(location)

        super().__init__(iterable=[
            Action('e2', value),
            Action('e1', value)
        ])
