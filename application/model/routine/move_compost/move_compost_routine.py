from typing import Literal

from application.model.action.activate_compost_loop_source_action_set import ActivateCompostLoopSourceActionSet
from application.model.action.set_rotary_valve_compost_loop_action_set import SetRotaryValveCompostLoopActionSet
from application.model.action.set_rotary_valve_from_air_loop_action_set import SetRotaryValveFromAirLoopActionSet
from application.model.action.set_rotary_valve_to_air_loop_action_set import SetRotaryValveToAirLoopActionSet
from application.model.action.switch_air_hammer_action_set import SwitchAirHammerActionSet
from application.model.action.switch_air_loop_bypass_sensor_loop_action_set import \
    SwitchAirLoopBypassSensorLoopActionSet
from application.model.action.switch_air_mover_action_set import SwitchAirMoverActionSet
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep
from application.model.state.isolation.compost_loop_bioreactor_1_state import CompostLoopBioreactor1State
from application.model.state.isolation.compost_loop_bioreactor_2_state import CompostLoopBioreactor2State
from application.model.state.isolation.compost_loop_bsf_reproduction_state import CompostLoopBSFReproductionState
from application.model.state.isolation.compost_loop_shredder_storage_state import CompostLoopShredderStorageState


class MoveCompostRoutine(Routine):
    name = "MoveCompostRoutine"

    def __init__(self,
                 from_location: Literal['shredder_storage', 'bioreactor1', 'bioreactor2', 'bsf_reproduction'],
                 to_location: Literal['shredder_storage', 'bioreactor1', 'bioreactor2', 'bsf_reproduction', 'sieve'],
                 ):

        must_run_in_state = {
            'shredder_storage': CompostLoopShredderStorageState,
            'bioreactor1': CompostLoopBioreactor1State,
            'bioreactor2': CompostLoopBioreactor2State,
            'bsf_reproduction': CompostLoopBSFReproductionState,
        }.get(from_location)

        super().__init__(
            steps=[
                # Bypass the sensor loop entirely
                RoutineStep(SwitchAirLoopBypassSensorLoopActionSet('divert'), then_wait_n_sec=0),

                # Open the butterfly valve and pressurize the container to release the compost
                RoutineStep(ActivateCompostLoopSourceActionSet(from_location), then_wait_n_sec=00),
                RoutineStep(SwitchAirMoverActionSet('on'), then_wait_n_sec=30),
                # Run the air hammer briefly (it is VERY loud)
                RoutineStep(SwitchAirHammerActionSet(from_location, 'open'), then_wait_n_sec=1),
                RoutineStep(SwitchAirHammerActionSet(from_location, 'close'), then_wait_n_sec=10),
                # Turn the air off and close the butterfly valve
                RoutineStep(SwitchAirMoverActionSet('off'), then_wait_n_sec=10),
                RoutineStep(ActivateCompostLoopSourceActionSet(deactivate=True), then_wait_n_sec=0),
                # Push the compost through
                RoutineStep(SetRotaryValveFromAirLoopActionSet('compost_loop'), then_wait_n_sec=0),
                RoutineStep(SetRotaryValveCompostLoopActionSet(to_location), then_wait_n_sec=0),
                RoutineStep(SetRotaryValveToAirLoopActionSet(to_location), then_wait_n_sec=0),
                RoutineStep(SwitchAirMoverActionSet('on'), then_wait_n_sec=30),
                RoutineStep(SwitchAirMoverActionSet('off'), then_wait_n_sec=10),

                # Repeat this cycle two more times
                RoutineStep(SetRotaryValveFromAirLoopActionSet(from_location), then_wait_n_sec=0),
                RoutineStep(SetRotaryValveCompostLoopActionSet('air_loop'), then_wait_n_sec=0),
                RoutineStep(SetRotaryValveToAirLoopActionSet('compost_loop'), then_wait_n_sec=0),
                RoutineStep(ActivateCompostLoopSourceActionSet(from_location), then_wait_n_sec=00),
                RoutineStep(SwitchAirMoverActionSet('on'), then_wait_n_sec=30),
                RoutineStep(SwitchAirHammerActionSet(from_location, 'open'), then_wait_n_sec=1),
                RoutineStep(SwitchAirHammerActionSet(from_location, 'close'), then_wait_n_sec=10),
                RoutineStep(SwitchAirMoverActionSet('off'), then_wait_n_sec=10),
                RoutineStep(ActivateCompostLoopSourceActionSet(deactivate=True), then_wait_n_sec=0),
                RoutineStep(SetRotaryValveFromAirLoopActionSet('compost_loop'), then_wait_n_sec=0),
                RoutineStep(SetRotaryValveCompostLoopActionSet(to_location), then_wait_n_sec=0),
                RoutineStep(SetRotaryValveToAirLoopActionSet(to_location), then_wait_n_sec=0),
                RoutineStep(SwitchAirMoverActionSet('on'), then_wait_n_sec=30),
                RoutineStep(SwitchAirMoverActionSet('off'), then_wait_n_sec=10),

                RoutineStep(SetRotaryValveFromAirLoopActionSet(from_location), then_wait_n_sec=0),
                RoutineStep(SetRotaryValveCompostLoopActionSet('air_loop'), then_wait_n_sec=0),
                RoutineStep(SetRotaryValveToAirLoopActionSet('compost_loop'), then_wait_n_sec=0),
                RoutineStep(ActivateCompostLoopSourceActionSet(from_location), then_wait_n_sec=00),
                RoutineStep(SwitchAirMoverActionSet('on'), then_wait_n_sec=30),
                RoutineStep(SwitchAirHammerActionSet(from_location, 'open'), then_wait_n_sec=1),
                RoutineStep(SwitchAirHammerActionSet(from_location, 'close'), then_wait_n_sec=10),
                RoutineStep(SwitchAirMoverActionSet('off'), then_wait_n_sec=10),
                RoutineStep(ActivateCompostLoopSourceActionSet(deactivate=True), then_wait_n_sec=0),
                RoutineStep(SetRotaryValveFromAirLoopActionSet('compost_loop'), then_wait_n_sec=0),
                RoutineStep(SetRotaryValveCompostLoopActionSet(to_location), then_wait_n_sec=0),
                RoutineStep(SetRotaryValveToAirLoopActionSet(to_location), then_wait_n_sec=0),
                RoutineStep(SwitchAirMoverActionSet('on'), then_wait_n_sec=30),
                RoutineStep(SwitchAirMoverActionSet('off'), then_wait_n_sec=10),

                # End sequence
                RoutineStep(SetRotaryValveFromAirLoopActionSet(from_location), then_wait_n_sec=0),
                RoutineStep(SetRotaryValveCompostLoopActionSet('air_loop'), then_wait_n_sec=0),
                RoutineStep(SetRotaryValveToAirLoopActionSet('compost_loop'), then_wait_n_sec=0),
                RoutineStep(SwitchAirLoopBypassSensorLoopActionSet('through'), then_wait_n_sec=0),
            ],
            must_run_in_state=must_run_in_state,
            failure_recovery_steps=[
                RoutineStep(SwitchAirHammerActionSet(from_location, 'close'), then_wait_n_sec=0),
                RoutineStep(SwitchAirMoverActionSet('off'), then_wait_n_sec=10),
                RoutineStep(ActivateCompostLoopSourceActionSet(deactivate=True), then_wait_n_sec=0),
                RoutineStep(SetRotaryValveFromAirLoopActionSet(from_location), then_wait_n_sec=0),
                RoutineStep(SetRotaryValveCompostLoopActionSet('air_loop'), then_wait_n_sec=0),
                RoutineStep(SetRotaryValveToAirLoopActionSet('compost_loop'), then_wait_n_sec=0),
                RoutineStep(SwitchAirLoopBypassSensorLoopActionSet('through'), then_wait_n_sec=0),
            ]
        )
