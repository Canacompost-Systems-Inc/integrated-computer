from typing import Literal

from application.model.action.action import Action
from application.model.action.action_set import ActionSet


class SwitchAirMoverActionSet(ActionSet):

    def __init__(self,
                 to: Literal['on', 'off'] = 'on',
                 strength='50'
                 ):

        # TODO - strength needs to be inverted, so maybe pass in an int and convert it to the nearest inverse value

        if to == 'off':
            strength = '100'

        super().__init__(iterable=[
            # Action('f4', strength),
            Action('f1', to)
        ])
