from application.model.action.switch_air_loop_bypass_sensor_loop_action_set import \
    SwitchAirLoopBypassSensorLoopActionSet
from application.model.action.switch_air_loop_environment_exchange_action_set import \
    SwitchAirLoopEnvironmentExchangeActionSet
from application.model.action.switch_air_mover_action_set import SwitchAirMoverActionSet
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep


class FlushCompostLoopRoutine(Routine):
    name = "FlushCompostLoopRoutine"

    def __init__(self):

        super().__init__(
            steps=[
                # We are skipping the sensor loop
                RoutineStep(SwitchAirLoopBypassSensorLoopActionSet('divert'), duration_sec=0),
                # Will flush to the environment
                RoutineStep(SwitchAirLoopEnvironmentExchangeActionSet(strength='100'), duration_sec=0),
                # Begin circulating the air
                RoutineStep(SwitchAirMoverActionSet('on', strength='50'), duration_sec=30),
                # End sequence
                RoutineStep(SwitchAirLoopEnvironmentExchangeActionSet(strength='0'), duration_sec=0),
                RoutineStep(SwitchAirMoverActionSet('off'), duration_sec=0),
            ],
            available_in_states=[]
        )
