from typing import Literal

from application.model.action.action import Action
from application.model.action.action_set import ActionSet


class ActivateCompostLoopSourceActionSet(ActionSet):

    def __init__(self,
                 location: Literal['shredder_storage', 'bioreactor1', 'bioreactor2', 'bsf_reproduction',
                                   'none'] = 'none',
                 deactivate: bool = True,
                 ):

        if deactivate:
            location = 'none'
            new_state = 'close'
        else:
            new_state = 'open'

        location_mapping = {
            'shredder_storage': 'e3',
            'bioreactor1': 'e4',
            'bioreactor2': 'e5',
            'bsf_reproduction': 'e6',
            'none': 'e3,e4,e5,e6',
        }
        butterfly_valve_device_ids = location_mapping.get(location).split(',')

        super().__init__(iterable=[
            Action(butterfly_valve_device_id, new_state)
            for butterfly_valve_device_id in butterfly_valve_device_ids
        ])
