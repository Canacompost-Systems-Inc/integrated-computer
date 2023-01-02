from application.model.action.switch_water_pump_action_set import SwitchWaterPumpActionSet
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep


class HumidifyShredderStorageRoutine(Routine):
    name = "HumidifyShredderStorageRoutine"

    def __init__(self):

        super().__init__(
            steps=[
                RoutineStep(SwitchWaterPumpActionSet('shredder_storage', 'open'), duration_sec=5),
                # End sequence
                RoutineStep(SwitchWaterPumpActionSet('shredder_storage', 'close'), duration_sec=0),
            ],
            available_in_states=[]
        )
