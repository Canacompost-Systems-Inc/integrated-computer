from application.model.action.switch_water_pump_action_set import SwitchWaterPumpActionSet
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep


class HumidifyBSFReproductionRoutine(Routine):
    name = "HumidifyBSFReproductionRoutine"

    def __init__(self):

        super().__init__(
            steps=[
                RoutineStep(SwitchWaterPumpActionSet('bsf_reproduction', 'open'), duration_sec=5),
                # End sequence
                RoutineStep(SwitchWaterPumpActionSet('bsf_reproduction', 'close'), duration_sec=0),
            ],
            available_in_states=[]
        )
