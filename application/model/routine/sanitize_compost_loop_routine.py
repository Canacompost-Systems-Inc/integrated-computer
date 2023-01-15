from application.model.action.switch_air_loop_bypass_sensor_loop_action_set import \
    SwitchAirLoopBypassSensorLoopActionSet
from application.model.action.switch_air_loop_environment_exchange_action_set import \
    SwitchAirLoopEnvironmentExchangeActionSet
from application.model.action.switch_air_mover_action_set import SwitchAirMoverActionSet
from application.model.action.switch_ozone_generator_action_set import SwitchOzoneGeneratorActionSet
from application.model.action.switch_uvc_light_action_set import SwitchUVCLightActionSet
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep


class SanitizeCompostLoopRoutine(Routine):
    name = "SanitizeCompostLoopRoutine"

    def __init__(self):

        super().__init__(
            steps=[
                # We are skipping the sensor loop
                RoutineStep(SwitchAirLoopBypassSensorLoopActionSet('divert'), then_wait_n_sec=0),
                # Turn on the ozone generator and let it build up
                # NOTE - commenting this out while we have air leaks
                # RoutineStep(SwitchOzoneGeneratorActionSet('on'), then_wait_n_sec=30),
                # Turn on the UVC light
                RoutineStep(SwitchUVCLightActionSet('on'), then_wait_n_sec=0),
                # Begin circulating the ozone
                RoutineStep(SwitchAirMoverActionSet('on'), then_wait_n_sec=10),
                # Stop producing ozone
                RoutineStep(SwitchOzoneGeneratorActionSet('off'), then_wait_n_sec=0),
                # Flush the ozone from the system
                RoutineStep(SwitchAirLoopEnvironmentExchangeActionSet(strength='100'), then_wait_n_sec=30),
                # End sequence
                RoutineStep(SwitchUVCLightActionSet('off'), then_wait_n_sec=0),
                RoutineStep(SwitchAirLoopEnvironmentExchangeActionSet(strength='0'), then_wait_n_sec=0),
                RoutineStep(SwitchAirMoverActionSet('off'), then_wait_n_sec=10),
            ],
            must_run_in_state=None,
            failure_recovery_steps=[
                RoutineStep(SwitchUVCLightActionSet('off'), then_wait_n_sec=0),
                RoutineStep(SwitchOzoneGeneratorActionSet('off'), then_wait_n_sec=10),
                RoutineStep(SwitchAirLoopEnvironmentExchangeActionSet(strength='100'), then_wait_n_sec=30),
                RoutineStep(SwitchAirLoopEnvironmentExchangeActionSet(strength='0'), then_wait_n_sec=0),
                RoutineStep(SwitchAirMoverActionSet('off'), then_wait_n_sec=10),
            ]
        )
