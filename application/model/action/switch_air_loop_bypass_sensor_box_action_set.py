from typing import Literal

from application.model.action.action import Action
from application.model.action.action_set import ActionSet


class SwitchAirLoopBypassSensorBoxActionSet(ActionSet):

    def __init__(self,
                 to: Literal['divert', 'through'] = 'through',
                 ):

        super().__init__(iterable=[
          # TODO - ask Leo if we will add this back. For now, it is not connected to the MCU
            # Action('ea', to)
        ])
