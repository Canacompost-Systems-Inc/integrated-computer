from typing import Literal

from application.model.action.action import Action
from application.model.action.action_set import ActionSet


class SwitchHeaterActionSet(ActionSet):

    def __init__(self,
                 location: Literal['shredder_storage', 'bioreactor1', 'bioreactor2', 'bsf_reproduction'],
                 to: Literal['open', 'close'] = 'close',
                 ):

        location_mapping = {
            'shredder_storage': 'f5',
            'bioreactor1': 'f7',
            'bioreactor2': 'f9',
            'bsf_reproduction': 'fb'
        }
        value = location_mapping.get(location)

        super().__init__(iterable=[
            Action(value, to)
        ])
