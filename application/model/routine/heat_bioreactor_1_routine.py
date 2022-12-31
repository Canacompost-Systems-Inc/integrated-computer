from application.model.action.switch_heater_action_set import SwitchHeaterActionSet
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep


class HeatBioreactor1Routine(Routine):
    name = "HeatBioreactor1Routine"

    def __init__(self):

        super().__init__(
            steps=[
                RoutineStep(SwitchHeaterActionSet('bioreactor1', 'open'), duration_sec=15),
                # End sequence
                RoutineStep(SwitchHeaterActionSet('bioreactor1', 'close'), duration_sec=0),
            ],
            available_in_states=[]
        )
