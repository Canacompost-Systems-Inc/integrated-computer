from collections import UserList
from typing import List, Optional

from application.model.routine.routine_step import RoutineStep
from application.model.state.isolation.isolation_state import IsolationState


class Routine(UserList):
    name = "Routine"

    def __init__(self,
                 steps: List[Optional[RoutineStep]],
                 failure_recovery_steps: Optional[List[RoutineStep]] = None,
                 must_run_in_state: Optional[type[IsolationState]] = None,
                 ):

        super().__init__(steps)

        self.failure_recovery_steps = failure_recovery_steps
        self.must_run_in_state = must_run_in_state

    def __eq__(self, other):
        return getattr(self, 'name', None) == getattr(other, 'name', None)

    def can_run_in_state(self, isolation_state: IsolationState):
        if self.must_run_in_state is None:
            # Any state is valid
            return True
        # TODO - make sure this works without isolation_state.name in [list of names]
        return isolation_state.name == self.must_run_in_state.name
