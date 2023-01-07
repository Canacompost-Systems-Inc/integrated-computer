from typing import Literal

from application.model.action.action import Action
from application.model.action.action_set import ActionSet


class SwitchAirLoopBypassSensorLoopActionSet(ActionSet):

    def __init__(self,
                 to: Literal['divert', 'through'] = 'through',
                 ):

        super().__init__(iterable=[
            Action('e7', to)
        ])
