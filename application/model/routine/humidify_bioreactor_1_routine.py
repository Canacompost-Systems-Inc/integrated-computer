from application.model.action.switch_water_pump_action_set import SwitchWaterPumpActionSet
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep


class HumidifyBioreactor1Routine(Routine):
    name = "HumidifyBioreactor1Routine"

    def __init__(self):

        super().__init__(
            steps=[
                RoutineStep(SwitchWaterPumpActionSet('bioreactor1', 'open'), duration_sec=5),
                # End sequence
                RoutineStep(SwitchWaterPumpActionSet('bioreactor1', 'close'), duration_sec=0),
            ],
            available_in_states=[]
        )
