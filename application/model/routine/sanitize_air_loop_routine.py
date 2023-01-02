from application.model.action.switch_air_loop_bypass_radiator_dehumidifier_action_set import \
    SwitchAirLoopBypassRadiatorDehumidifierActionSet
from application.model.action.switch_air_loop_bypass_sensor_box_action_set import SwitchAirLoopBypassSensorBoxActionSet
from application.model.action.switch_air_loop_bypass_sensor_loop_action_set import \
    SwitchAirLoopBypassSensorLoopActionSet
from application.model.action.switch_air_mover_action_set import SwitchAirMoverActionSet
from application.model.action.switch_ozone_generator_action_set import SwitchOzoneGeneratorActionSet
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep
from application.model.state.isolation.default_state import DefaultState


class SanitizeAirLoopRoutine(Routine):
    name = "SanitizeAirLoopRoutine"

    def __init__(self):

        super().__init__(
            steps=[
                # Remove any bypasses
                RoutineStep(SwitchAirLoopBypassSensorLoopActionSet('divert'), duration_sec=0),
                # Turn on the ozone generator and let it build up
                RoutineStep(SwitchOzoneGeneratorActionSet('on'), duration_sec=30),
                # Begin circulating the ozone
                RoutineStep(SwitchAirMoverActionSet('on', strength='50per'), duration_sec=10),
                # End sequence
                RoutineStep(SwitchOzoneGeneratorActionSet('off'), duration_sec=10),
                RoutineStep(SwitchAirLoopBypassSensorLoopActionSet('through'), duration_sec=0),
                RoutineStep(SwitchAirMoverActionSet('off'), duration_sec=0),
            ],
            available_in_states=[
                DefaultState,
            ]
        )
