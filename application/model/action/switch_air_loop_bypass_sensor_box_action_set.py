from typing import Literal

from application.model.action.action import Action
from application.model.action.action_set import ActionSet


class SwitchAirLoopBypassSensorBoxActionSet(ActionSet):

    def __init__(self,
                 to: Literal['divert', 'through'] = 'through',
                 ):

        super().__init__(iterable=[
            # This is permanently removed, so we just won't do this action
            # Action('ea', to)
        ])
