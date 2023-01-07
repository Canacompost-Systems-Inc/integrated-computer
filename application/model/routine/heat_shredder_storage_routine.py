from application.model.action.switch_heater_action_set import SwitchHeaterActionSet
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep


class HeatShredderStorageRoutine(Routine):
    name = "HeatShredderStorageRoutine"

    def __init__(self):

        super().__init__(
            steps=[
                RoutineStep(SwitchHeaterActionSet('shredder_storage', 'open'), then_wait_n_sec=15),
                # End sequence
                RoutineStep(SwitchHeaterActionSet('shredder_storage', 'close'), then_wait_n_sec=0),
            ],
            must_run_in_state=None
        )
