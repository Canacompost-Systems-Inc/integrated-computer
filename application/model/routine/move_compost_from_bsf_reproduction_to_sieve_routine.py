from application.model.action.activate_compost_loop_destination_action_set import \
    ActivateCompostLoopDestinationActionSet
from application.model.action.switch_air_loop_bypass_sensor_box_action_set import SwitchAirLoopBypassSensorBoxActionSet
from application.model.action.switch_air_loop_bypass_sensor_loop_action_set import \
    SwitchAirLoopBypassSensorLoopActionSet
from application.model.action.switch_air_mover_action_set import SwitchAirMoverActionSet
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep
from application.model.state.isolation.compost_loop_bsf_reproduction_state import CompostLoopBSFReproductionState


class MoveCompostFromBSFReproductionToSieveRoutine(Routine):
    name = "MoveCompostFromBSFReproductionToSieveRoutine"

    def __init__(self):

        super().__init__(
            steps=[
                # Bypass the sensor loop entirely
                RoutineStep(SwitchAirLoopBypassSensorLoopActionSet('divert'), then_wait_n_sec=0),
                # Open the compost destination
                RoutineStep(ActivateCompostLoopDestinationActionSet('sieve'), then_wait_n_sec=0),
                # Begin circulating the air
                RoutineStep(SwitchAirMoverActionSet('on'), then_wait_n_sec=30),
                # End sequence
                RoutineStep(SwitchAirMoverActionSet('off'), then_wait_n_sec=10),
                RoutineStep(SwitchAirLoopBypassSensorBoxActionSet('through'), then_wait_n_sec=0),
            ],
            must_run_in_state=CompostLoopBSFReproductionState
        )
