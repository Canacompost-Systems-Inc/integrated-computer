from typing import Dict

from application.model.action.activate_air_loop_action_set import ActivateAirLoopActionSet
from application.model.location.airloop_location import AirLoopLocation
from application.model.location.base_location import BaseLocation
from application.model.location.bioreactor2_location import Bioreactor2Location
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep
from application.model.state.isolation.isolation_state import IsolationState


class AirLoopBioreactor2State(IsolationState):
    name = "AirLoopBioreactor2State"

    @property
    def location_sensor_remapping(self) -> Dict[type(BaseLocation), type(BaseLocation)]:
        return {
            AirLoopLocation: Bioreactor2Location,
        }

    def activate_state(self):
        return Routine(steps=[
            RoutineStep(ActivateAirLoopActionSet('bioreactor2'), then_wait_n_sec=0),
        ])

    def deactivate_state(self):
        return Routine(steps=[
            RoutineStep(ActivateAirLoopActionSet('compost_loop'), then_wait_n_sec=0),
        ])
