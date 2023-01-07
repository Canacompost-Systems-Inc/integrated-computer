from application.model.action.switch_heater_action_set import SwitchHeaterActionSet
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep


class HeatBioreactor1Routine(Routine):
    name = "HeatBioreactor1Routine"

    def __init__(self):

        super().__init__(
            steps=[
                RoutineStep(SwitchHeaterActionSet('bioreactor1', 'open'), then_wait_n_sec=15),
                # End sequence
                RoutineStep(SwitchHeaterActionSet('bioreactor1', 'close'), then_wait_n_sec=0),
            ],
            must_run_in_state=None
        )
