from application.model.action.switch_bsf_light_action_set import SwitchBSFLightActionSet
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep


class DissuadeReproductionRoutine(Routine):
    name = "DissuadeReproductionRoutine"

    def __init__(self):

        super().__init__(
            steps=[
                RoutineStep(SwitchBSFLightActionSet('bsf_reproduction', 'off'), then_wait_n_sec=0),
            ],
            must_run_in_state=None,
            failure_recovery_steps=[
                RoutineStep(SwitchBSFLightActionSet('bsf_reproduction', 'off'), then_wait_n_sec=0),
            ]
        )
