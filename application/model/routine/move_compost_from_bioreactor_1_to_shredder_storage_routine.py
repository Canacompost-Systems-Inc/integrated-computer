from application.model.action.activate_compost_loop_destination_action_set import \
    ActivateCompostLoopDestinationActionSet
from application.model.action.activate_compost_loop_source_action_set import ActivateCompostLoopSourceActionSet
from application.model.action.switch_air_hammer_action_set import SwitchAirHammerActionSet
from application.model.action.switch_air_loop_bypass_sensor_loop_action_set import \
    SwitchAirLoopBypassSensorLoopActionSet
from application.model.action.switch_air_mover_action_set import SwitchAirMoverActionSet
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep
from application.model.state.isolation.compost_loop_bioreactor_1_state import CompostLoopBioreactor1State


class MoveCompostFromBioreactor1ToShredderStorageRoutine(Routine):
    name = "MoveCompostFromBioreactor1ToShredderStorageRoutine"

    def __init__(self):

        super().__init__(
            steps=[
                # Bypass the sensor loop entirely
                RoutineStep(SwitchAirLoopBypassSensorLoopActionSet('divert'), then_wait_n_sec=0),
                # Open the compost destination
                RoutineStep(ActivateCompostLoopDestinationActionSet('shredder_storage'), then_wait_n_sec=0),
                # Run the air hammer briefly (it is VERY loud)
                RoutineStep(SwitchAirHammerActionSet('bioreactor1', 'open'), then_wait_n_sec=1),
                RoutineStep(SwitchAirHammerActionSet('bioreactor1', 'close'), then_wait_n_sec=0),
                # Begin circulating the air and move as much compost as possible
                RoutineStep(SwitchAirMoverActionSet('on'), then_wait_n_sec=30),
                # Turn the air off to let the remaining compost drop down
                RoutineStep(SwitchAirMoverActionSet('off'), then_wait_n_sec=10),
                # Run the air hammer briefly (it is VERY loud)
                RoutineStep(SwitchAirHammerActionSet('bioreactor1', 'open'), then_wait_n_sec=1),
                RoutineStep(SwitchAirHammerActionSet('bioreactor1', 'close'), then_wait_n_sec=0),
                # Close the butterfly valve, circulate air twice to move the remainder, and re-open butterfly valve
                RoutineStep(ActivateCompostLoopSourceActionSet(deactivate=True), then_wait_n_sec=0),
                RoutineStep(SwitchAirMoverActionSet('on'), then_wait_n_sec=15),
                RoutineStep(SwitchAirMoverActionSet('off'), then_wait_n_sec=10),
                RoutineStep(SwitchAirMoverActionSet('on'), then_wait_n_sec=15),
                RoutineStep(ActivateCompostLoopSourceActionSet('bioreactor1'), then_wait_n_sec=0),
                # End sequence
                RoutineStep(SwitchAirMoverActionSet('off'), then_wait_n_sec=10),
                RoutineStep(ActivateCompostLoopDestinationActionSet('air_loop'), then_wait_n_sec=0),
                RoutineStep(SwitchAirLoopBypassSensorLoopActionSet('through'), then_wait_n_sec=0),
            ],
            must_run_in_state=CompostLoopBioreactor1State,
            failure_recovery_steps=[
                RoutineStep(SwitchAirHammerActionSet('bioreactor1', 'close'), then_wait_n_sec=0),
                RoutineStep(SwitchAirMoverActionSet('off'), then_wait_n_sec=10),
                RoutineStep(ActivateCompostLoopSourceActionSet('bioreactor1'), then_wait_n_sec=0),
                RoutineStep(SwitchAirLoopBypassSensorLoopActionSet('through'), then_wait_n_sec=0),
            ]
        )