from application.model.action.switch_water_pump_action_set import SwitchWaterPumpActionSet
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep


class HumidifyBioreactor2Routine(Routine):
    name = "HumidifyBioreactor2Routine"

    def __init__(self):

        super().__init__(
            steps=[
                RoutineStep(SwitchWaterPumpActionSet('bioreactor2', 'open'), then_wait_n_sec=5),
                # End sequence
                RoutineStep(SwitchWaterPumpActionSet('bioreactor2', 'close'), then_wait_n_sec=0),
            ],
            must_run_in_state=None,
            failure_recovery_steps=[
                RoutineStep(SwitchWaterPumpActionSet('bioreactor2', 'close'), then_wait_n_sec=0),
            ]
        )
