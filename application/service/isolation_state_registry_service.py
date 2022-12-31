from typing import List

from application import IsolationContext
from application.model.state.isolation.isolation_state import IsolationState


class IsolationStateRegistryService:
    """
    Isolation states are characterized by the shared air loop or compost loop being 'contaminated' by the contents of a
    container (i.e. bioreactor, shredder storage, etc.). Only one can be active at a time, and the shared infrastructure
    must be flushed when changing between isolation states.
    """

    def __init__(self, isolation_state_list: List[type[IsolationState]], isolation_context: IsolationContext):

        self.isolation_state_map = {
            isolation_state.name: isolation_state(isolation_context)
            for isolation_state
            in isolation_state_list
        }

    def all_isolation_states(self) -> List[IsolationState]:
        return list(self.isolation_state_map.values())

    def get_isolation_state(self, isolation_state_name: str) -> IsolationState:
        if isolation_state_name not in self.isolation_state_map:
            raise ValueError(f"Isolation State name '{isolation_state_name}' is not registered")
        return self.isolation_state_map.get(isolation_state_name, None)
