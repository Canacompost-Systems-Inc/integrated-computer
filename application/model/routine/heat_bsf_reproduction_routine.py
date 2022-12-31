from application.model.action.switch_heater_action_set import SwitchHeaterActionSet
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep


class HeatBSFReproductionRoutine(Routine):
    name = "HeatBSFReproductionRoutine"

    def __init__(self):

        super().__init__(
            steps=[
                RoutineStep(SwitchHeaterActionSet('bsf_reproduction', 'open'), duration_sec=15),
                # End sequence
                RoutineStep(SwitchHeaterActionSet('bsf_reproduction', 'close'), duration_sec=0),
            ],
            available_in_states=[]
        )
