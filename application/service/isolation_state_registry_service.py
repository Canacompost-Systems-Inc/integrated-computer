from typing import List

from application import IsolationContext
from application.model.state.isolation.isolation_state import IsolationState


class IsolationStateRegistryService:

    def __init__(self, isolation_state_list: List[type[IsolationState]], isolation_context: IsolationContext):

        self.isolation_state_map = {
            isolation_state.name: isolation_state(isolation_context)
            for isolation_state
            in isolation_state_list
        }
