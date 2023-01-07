from typing import Literal

from application.model.action.action import Action
from application.model.action.action_set import ActionSet


class SwitchAirHammerActionSet(ActionSet):

    def __init__(self,
                 location: Literal['shredder_storage', 'bioreactor1', 'bioreactor2', 'bsf_reproduction'],
                 to: Literal['open', 'close'] = 'close',
                 ):

        location_mapping = {
            'shredder_storage': 'ed',
            'bioreactor1': 'ee',
            'bioreactor2': 'ef',
            'bsf_reproduction': 'f0'
        }
        value = location_mapping.get(location)

        super().__init__(iterable=[
            Action(value, to)
        ])
