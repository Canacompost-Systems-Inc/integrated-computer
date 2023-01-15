from application.model.action.read_sensors_air_loop_realtime_action_set import ReadSensorsAirLoopRealTimeActionSet
from application.model.action.read_sensors_container_action_set import ReadSensorsContainerActionSet
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep


class ReadSensorsRealtimeRoutine(Routine):
    name = "ReadSensorsRealtimeRoutine"

    def __init__(self):

        super().__init__(
            steps=[
                # Read the realtime sensors from the airloop and bioreactors
                RoutineStep(ReadSensorsAirLoopRealTimeActionSet(), then_wait_n_sec=0),
                RoutineStep(ReadSensorsContainerActionSet('shredder_storage'), then_wait_n_sec=0),
                RoutineStep(ReadSensorsContainerActionSet('bioreactor1'), then_wait_n_sec=0),
                RoutineStep(ReadSensorsContainerActionSet('bioreactor2'), then_wait_n_sec=0),
                RoutineStep(ReadSensorsContainerActionSet('bsf_reproduction'), then_wait_n_sec=0),
            ],
            must_run_in_state=None,
            failure_recovery_steps=[
            ]
        )
