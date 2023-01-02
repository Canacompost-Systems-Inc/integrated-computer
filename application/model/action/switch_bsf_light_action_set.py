from typing import Literal

from application.model.action.action import Action
from application.model.action.action_set import ActionSet


class SwitchBSFLightActionSet(ActionSet):

    def __init__(self,
                 location: Literal['bsf_reproduction'] = 'bsf_reproduction',
                 to: Literal['on', 'off'] = 'off',
                 ):

        location_mapping = {
            'bsf_reproduction': 'f2'
        }
        value = location_mapping.get(location)

        super().__init__(iterable=[
            Action(value, to)
        ])
