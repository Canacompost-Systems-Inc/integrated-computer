from typing import List

from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep


class AdvancedTabRoutine(Routine):
    name = "AdvancedTabRoutine"

    def __init__(self, steps: List[RoutineStep]):

        super().__init__(
            steps=steps,
            available_in_states=[]
        )
