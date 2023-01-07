from typing import Dict

from application.model.action.activate_air_loop_action_set import ActivateAirLoopActionSet
from application.model.location.airloop_location import AirLoopLocation
from application.model.location.base_location import BaseLocation
from application.model.location.sieve_location import SieveLocation
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep
from application.model.state.isolation.isolation_state import IsolationState


class AirLoopSieveState(IsolationState):
    name = "AirLoopSieveState"

    @property
    def location_sensor_remapping(self) -> Dict[type(BaseLocation), type(BaseLocation)]:
        return {
            AirLoopLocation: SieveLocation,
        }

    def activate_state(self):
        return Routine(steps=[
            RoutineStep(ActivateAirLoopActionSet('sieve'), then_wait_n_sec=0),
        ])

    def deactivate_state(self):
        return Routine(steps=[
            RoutineStep(ActivateAirLoopActionSet('compost_loop'), then_wait_n_sec=0),
        ])
