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
                # # We are skipping the sensor loop
                # RoutineStep(SwitchAirLoopBypassSensorLoopActionSet('divert'), then_wait_n_sec=0),
                # # Will flush to the environment
                # RoutineStep(SwitchAirLoopEnvironmentExchangeActionSet(strength='100'), then_wait_n_sec=0),
                # # Begin circulating the air
                # RoutineStep(SwitchAirMoverActionSet('on'), then_wait_n_sec=30),
                # # End sequence
                # RoutineStep(SwitchAirLoopEnvironmentExchangeActionSet(strength='0'), then_wait_n_sec=0),
                # RoutineStep(SwitchAirMoverActionSet('off'), then_wait_n_sec=10),
                # RoutineStep(SwitchAirLoopBypassSensorLoopActionSet('through'), then_wait_n_sec=0),
            ],
            must_run_in_state=None,
            failure_recovery_steps=[
                RoutineStep(SwitchAirLoopEnvironmentExchangeActionSet(strength='0'), then_wait_n_sec=0),
                RoutineStep(SwitchAirMoverActionSet('off'), then_wait_n_sec=10),
                RoutineStep(SwitchAirLoopBypassSensorLoopActionSet('through'), then_wait_n_sec=0),
            ]
        )
