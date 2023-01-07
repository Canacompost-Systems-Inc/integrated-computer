from application.model.action.switch_air_loop_bypass_radiator_dehumidifier_action_set import \
    SwitchAirLoopBypassRadiatorDehumidifierActionSet
from application.model.action.switch_air_loop_bypass_sensor_box_action_set import SwitchAirLoopBypassSensorBoxActionSet
from application.model.action.switch_air_loop_bypass_sensor_loop_action_set import \
    SwitchAirLoopBypassSensorLoopActionSet
from application.model.action.switch_air_mover_action_set import SwitchAirMoverActionSet
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep
from application.model.state.isolation.air_loop_shredder_storage_state import AirLoopShredderStorageState


class CoolAndDehumidifyShredderStorageRoutine(Routine):
    name = "CoolAndDehumidifyShredderStorageRoutine"

    def __init__(self):

        super().__init__(
            steps=[
                # Bypass the sensor box but not the radiator and dehumidifier
                RoutineStep(SwitchAirLoopBypassSensorLoopActionSet('through'), then_wait_n_sec=0),
                RoutineStep(SwitchAirLoopBypassRadiatorDehumidifierActionSet('through'), then_wait_n_sec=0),
                RoutineStep(SwitchAirLoopBypassSensorBoxActionSet('divert'), then_wait_n_sec=0),
                # Begin circulating the air
                RoutineStep(SwitchAirMoverActionSet('on'), then_wait_n_sec=30),
                # End sequence
                RoutineStep(SwitchAirLoopBypassSensorBoxActionSet('through'), then_wait_n_sec=0),
                RoutineStep(SwitchAirMoverActionSet('off'), then_wait_n_sec=10),
            ],
            must_run_in_state=AirLoopShredderStorageState,
            failure_recovery_steps=[
                RoutineStep(SwitchAirLoopBypassSensorBoxActionSet('through'), then_wait_n_sec=0),
                RoutineStep(SwitchAirMoverActionSet('off'), then_wait_n_sec=10),
            ]
        )
