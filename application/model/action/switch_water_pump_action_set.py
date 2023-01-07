from typing import Literal

from application.model.action.action import Action
from application.model.action.action_set import ActionSet


class SwitchWaterPumpActionSet(ActionSet):

    def __init__(self,
                 location: Literal['shredder_storage', 'bioreactor1', 'bioreactor2', 'bsf_reproduction'],
                 to: Literal['open', 'close'] = 'close',
                 ):

        location_mapping = {
            'shredder_storage': 'f6',
            'bioreactor1': 'f8',
            'bioreactor2': 'fa',
            'bsf_reproduction': 'e9'
        }
        value = location_mapping.get(location)

        super().__init__(iterable=[
            Action(value, to)
        ])
