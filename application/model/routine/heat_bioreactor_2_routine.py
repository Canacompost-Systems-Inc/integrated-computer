from application.model.action.switch_heater_action_set import SwitchHeaterActionSet
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep


class HeatBioreactor2Routine(Routine):
    name = "HeatBioreactor2Routine"

    def __init__(self):

        super().__init__(
            steps=[
                RoutineStep(SwitchHeaterActionSet('bioreactor2', 'open'), duration_sec=15),
                # End sequence
                RoutineStep(SwitchHeaterActionSet('bioreactor2', 'close'), duration_sec=0),
            ],
            available_in_states=[]
        )
