from application.model.action.read_sensors_air_loop_action_set import ReadSensorsAirLoopActionSet
from application.model.action.read_sensors_container_action_set import ReadSensorsContainerActionSet
from application.model.action.switch_air_loop_bypass_radiator_dehumidifier_action_set import \
    SwitchAirLoopBypassRadiatorDehumidifierActionSet
from application.model.action.switch_air_loop_bypass_sensor_box_action_set import SwitchAirLoopBypassSensorBoxActionSet
from application.model.action.switch_air_loop_bypass_sensor_loop_action_set import \
    SwitchAirLoopBypassSensorLoopActionSet
from application.model.action.switch_air_mover_action_set import SwitchAirMoverActionSet
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep
from application.model.state.isolation.air_loop_bioreactor_2_state import AirLoopBioreactor2State


class ReadSensorsBioreactor2Routine(Routine):
    name = "ReadSensorsBioreactor2Routine"

    def __init__(self):

        super().__init__(
            steps=[
                # Bypass the radiator and dehumidifier but not the sensor box
                RoutineStep(SwitchAirLoopBypassSensorLoopActionSet('through'), duration_sec=0),
                RoutineStep(SwitchAirLoopBypassRadiatorDehumidifierActionSet('divert'), duration_sec=0),
                RoutineStep(SwitchAirLoopBypassSensorBoxActionSet('through'), duration_sec=0),
                # Begin circulating the air
                RoutineStep(SwitchAirMoverActionSet('on'), duration_sec=30),
                # Read from the sensor box and container
                RoutineStep(ReadSensorsContainerActionSet('bioreactor2'), duration_sec=0),
                RoutineStep(ReadSensorsAirLoopActionSet(), duration_sec=0),
                # End sequence
                RoutineStep(SwitchAirLoopBypassRadiatorDehumidifierActionSet('through'), duration_sec=0),
                RoutineStep(SwitchAirMoverActionSet('off'), duration_sec=0),
            ],
            available_in_states=[
                AirLoopBioreactor2State,
            ]
        )
