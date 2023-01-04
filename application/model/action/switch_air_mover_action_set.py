from typing import Literal

from application.model.action.action import Action
from application.model.action.action_set import ActionSet


class SwitchAirMoverActionSet(ActionSet):

    def __init__(self,
                 to: Literal['on', 'off'] = 'on'
                 ):

        super().__init__(iterable=[
            Action('f1', to)
        ])
