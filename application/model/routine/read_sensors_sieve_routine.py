from application.model.action.read_sensors_air_loop_action_set import ReadSensorsAirLoopActionSet
from application.model.action.switch_air_loop_bypass_radiator_dehumidifier_action_set import \
    SwitchAirLoopBypassRadiatorDehumidifierActionSet
from application.model.action.switch_air_loop_bypass_sensor_box_action_set import SwitchAirLoopBypassSensorBoxActionSet
from application.model.action.switch_air_loop_bypass_sensor_loop_action_set import \
    SwitchAirLoopBypassSensorLoopActionSet
from application.model.action.switch_air_mover_action_set import SwitchAirMoverActionSet
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep
from application.model.state.isolation.air_loop_sieve_state import AirLoopSieveState


class ReadSensorsSieveRoutine(Routine):
    name = "ReadSensorsSieveRoutine"

    def __init__(self):

        super().__init__(
            steps=[
                # Bypass the radiator and dehumidifier but not the sensor box
                RoutineStep(SwitchAirLoopBypassSensorLoopActionSet('through'), duration_sec=0),
                RoutineStep(SwitchAirLoopBypassRadiatorDehumidifierActionSet('divert'), duration_sec=0),
                RoutineStep(SwitchAirLoopBypassSensorBoxActionSet('through'), duration_sec=0),
                # Begin circulating the air
                RoutineStep(SwitchAirMoverActionSet('on', strength='50per'), duration_sec=30),
                # Read from the sensor box
                RoutineStep(ReadSensorsAirLoopActionSet(), duration_sec=0),
                # End sequence
                RoutineStep(SwitchAirLoopBypassRadiatorDehumidifierActionSet('through'), duration_sec=0),
                RoutineStep(SwitchAirMoverActionSet('off'), duration_sec=0),
            ],
            available_in_states=[
                AirLoopSieveState,
            ]
        )
