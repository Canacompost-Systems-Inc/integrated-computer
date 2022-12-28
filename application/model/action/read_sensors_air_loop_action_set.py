from typing import Literal

from application.model.action.action import Action
from application.model.action.action_set import ActionSet


class ReadSensorsAirLoopActionSet(ActionSet):

    def __init__(self):

        super().__init__(iterable=[
            Action('c7', None),  # Flow rate sensor
            Action('c9', None),  # O3 sensor
            Action('c0', None),
            Action('c1', None),
            Action('c2', None),
            Action('c8', None),
        ])
