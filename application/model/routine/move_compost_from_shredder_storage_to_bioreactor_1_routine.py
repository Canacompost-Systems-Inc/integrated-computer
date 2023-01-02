from application.model.action.activate_compost_loop_destination_action_set import \
    ActivateCompostLoopDestinationActionSet
from application.model.action.switch_air_loop_bypass_sensor_box_action_set import SwitchAirLoopBypassSensorBoxActionSet
from application.model.action.switch_air_loop_bypass_sensor_loop_action_set import \
    SwitchAirLoopBypassSensorLoopActionSet
from application.model.action.switch_air_mover_action_set import SwitchAirMoverActionSet
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep
from application.model.state.isolation.compost_loop_shredder_storage_state import CompostLoopShredderStorageState


class MoveCompostFromShredderStorageToBioreactor1Routine(Routine):
    name = "MoveCompostFromShredderStorageToBioreactor1Routine"

    def __init__(self):

        super().__init__(
            steps=[
                # Bypass the sensor loop entirely
                RoutineStep(SwitchAirLoopBypassSensorLoopActionSet('divert'), duration_sec=0),
                # Open the compost destination
                RoutineStep(ActivateCompostLoopDestinationActionSet('bioreactor1'), duration_sec=0),
                # Begin circulating the air
                RoutineStep(SwitchAirMoverActionSet('on', strength='50per'), duration_sec=30),
                # End sequence
                RoutineStep(SwitchAirMoverActionSet('off'), duration_sec=0),
                RoutineStep(SwitchAirLoopBypassSensorBoxActionSet('through'), duration_sec=0),
            ],
            available_in_states=[
                CompostLoopShredderStorageState,
            ]
        )
