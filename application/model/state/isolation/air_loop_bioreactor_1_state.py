from application.model.action.activate_air_loop_action_set import ActivateAirLoopActionSet
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep
from application.model.state.isolation.isolation_state import IsolationState


class AirLoopBioreactor1State(IsolationState):

    def activate_state(self):
        return Routine(steps=[
            RoutineStep(ActivateAirLoopActionSet('bioreactor1'), duration_sec=0),
        ])

    def deactivate_state(self):
        return Routine(steps=[
            RoutineStep(ActivateAirLoopActionSet('compost_loop'), duration_sec=0),
        ])
