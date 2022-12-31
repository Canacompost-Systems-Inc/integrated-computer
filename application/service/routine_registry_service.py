from typing import List

from application.model.routine.routine import Routine


class RoutineRegistryService:
    """
    Routines are sets of actions with timing and dependencies. This class registers the available routines, but does
    not perform them.
    """

    def __init__(self, routine_list: List[type(Routine)]):

        self.routine_map = {
            routine.name: routine()
            for routine
            in routine_list
        }

    def all_routines(self) -> List[Routine]:
        return list(self.routine_map.values())

    def get_routine(self, routine_name: str) -> Routine:
        if routine_name not in self.routine_map:
            raise ValueError(f"Routine name '{routine_name}' is not registered")
        return self.routine_map.get(routine_name, None)
