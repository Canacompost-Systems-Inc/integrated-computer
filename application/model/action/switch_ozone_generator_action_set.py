from typing import Literal

from application.model.action.action import Action
from application.model.action.action_set import ActionSet


class SwitchOzoneGeneratorActionSet(ActionSet):

    def __init__(self,
                 to: Literal['on', 'off'] = 'off',
                 ):

        super().__init__(iterable=[
            Action('f3', to)
        ])
