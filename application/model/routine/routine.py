from collections import UserList
from typing import List, Optional

from application.model.routine.routine_step import RoutineStep
from application.model.state.isolation.isolation_state import IsolationState


class Routine(UserList):
    name = "Routine"

    def __init__(self, steps: List[Optional[RoutineStep]], must_run_in_state: type[IsolationState] = None):

        super().__init__(steps)

        if must_run_in_state is None:
            must_run_in_state = []
        self.must_run_in_state = must_run_in_state

    def __eq__(self, other):
        return getattr(self, 'name', None) == getattr(other, 'name', None)

    def can_run_in_state(self, isolation_state: IsolationState):
        if len(self.must_run_in_state) == 0:
            # Any state is valid
            return True
        # TODO - make sure this works without isolation_state.name in [list of names]
        return isolation_state in self.must_run_in_state
