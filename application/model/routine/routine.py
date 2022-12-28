from collections import UserList
from typing import List, Optional

from application.model.routine.routine_step import RoutineStep
from application.model.state.isolation.isolation_state import IsolationState


class Routine(UserList):

    def __init__(self, steps: List[Optional[RoutineStep]], available_in_states: List[type[IsolationState]] = None):

        if available_in_states is None:
            available_in_states = []

        super(Routine).__init__(steps)

        self.available_in_states = [state.name for state in available_in_states]

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def can_run_in_state(self, isolation_state: IsolationState):
        if len(self.available_in_states) == 0:
            # Any state is valid
            return True
        return isolation_state.name in self.available_in_states
