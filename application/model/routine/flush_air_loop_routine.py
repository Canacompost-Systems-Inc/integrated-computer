from application.model.action.switch_air_loop_bypass_radiator_dehumidifier_action_set import \
    SwitchAirLoopBypassRadiatorDehumidifierActionSet
from application.model.action.switch_air_loop_bypass_sensor_box_action_set import SwitchAirLoopBypassSensorBoxActionSet
from application.model.action.switch_air_loop_bypass_sensor_loop_action_set import \
    SwitchAirLoopBypassSensorLoopActionSet
from application.model.action.switch_air_loop_environment_exchange_action_set import \
    SwitchAirLoopEnvironmentExchangeActionSet
from application.model.action.switch_air_mover_action_set import SwitchAirMoverActionSet
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep
from application.model.state.isolation.default_state import DefaultState


class FlushAirLoopRoutine(Routine):
    name = "FlushAirLoopRoutine"

    def __init__(self):

        super().__init__(
            steps=[
                # Remove any bypasses
                RoutineStep(SwitchAirLoopBypassSensorLoopActionSet('through'), duration_sec=0),
                RoutineStep(SwitchAirLoopBypassRadiatorDehumidifierActionSet('through'), duration_sec=0),
                RoutineStep(SwitchAirLoopBypassSensorBoxActionSet('through'), duration_sec=0),
                # Will flush to the environment
                RoutineStep(SwitchAirLoopEnvironmentExchangeActionSet(strength='100'), duration_sec=0),
                # Begin flushing
                RoutineStep(SwitchAirMoverActionSet('on', strength='50'), duration_sec=10),
                # Cycle through the air loop bypasses to flush each air path
                RoutineStep(SwitchAirLoopBypassSensorLoopActionSet('divert'), duration_sec=5),
                RoutineStep(SwitchAirLoopBypassSensorLoopActionSet('through'), duration_sec=0),
                RoutineStep(SwitchAirLoopBypassRadiatorDehumidifierActionSet('divert'), duration_sec=5),
                RoutineStep(SwitchAirLoopBypassRadiatorDehumidifierActionSet('through'), duration_sec=0),
                RoutineStep(SwitchAirLoopBypassSensorBoxActionSet('divert'), duration_sec=5),
                RoutineStep(SwitchAirLoopBypassSensorBoxActionSet('through'), duration_sec=0),
                # End sequence
                RoutineStep(SwitchAirLoopEnvironmentExchangeActionSet(strength='0'), duration_sec=0),
                RoutineStep(SwitchAirMoverActionSet('off'), duration_sec=0),
            ],
            available_in_states=[
                DefaultState,
            ]
        )
