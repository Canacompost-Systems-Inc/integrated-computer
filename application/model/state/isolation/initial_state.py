from typing import Dict

from application.model.action.action import Action
from application.model.action.action_set import ActionSet
from application.model.location.base_location import BaseLocation
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep
from application.model.state.isolation.isolation_state import IsolationState


class InitialState(IsolationState):
    """This state is only used during system startup. This may be removed once integration testing is done and the
    system starts up in the Default State."""
    name = "InitialState"

    @property
    def location_sensor_remapping(self) -> Dict[type(BaseLocation), type(BaseLocation)]:
        return {}

    def activate_state(self):
        return Routine(steps=[
            RoutineStep(ActionSet([Action('e0', 'ref')])),
            RoutineStep(ActionSet([Action('e1', 'ref')])),
            RoutineStep(ActionSet([Action('e2', 'ref')])),
        ])

    def deactivate_state(self):
        # Nothing is required to deactivate the default state
        return Routine(steps=[])
