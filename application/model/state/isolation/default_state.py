from application.model.action.activate_air_loop_action_set import ActivateAirLoopActionSet
from application.model.action.activate_compost_loop_destination_action_set import \
    ActivateCompostLoopDestinationActionSet
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep
from application.model.state.isolation.isolation_state import IsolationState


class DefaultState(IsolationState):

    def activate_state(self):
        return Routine(steps=[
            RoutineStep(ActivateCompostLoopDestinationActionSet('air_loop'), duration_sec=0),
            RoutineStep(ActivateAirLoopActionSet('compost_loop'), duration_sec=0),
        ])

    def deactivate_state(self):
        # Nothing is required to deactivate the default state
        return Routine(steps=[])
