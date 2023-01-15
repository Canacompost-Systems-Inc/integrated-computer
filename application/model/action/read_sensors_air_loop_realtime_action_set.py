from typing import Literal

from application.model.action.action import Action
from application.model.action.action_set import ActionSet


class ReadSensorsAirLoopRealTimeActionSet(ActionSet):

    def __init__(self):

        super().__init__(iterable=[
            # Action('c7', None),  # Flow rate sensor
            Action('c9', None),  # O3 sensor near generator
            Action('ca', None),  # O3 sensor in air loop
        ])
