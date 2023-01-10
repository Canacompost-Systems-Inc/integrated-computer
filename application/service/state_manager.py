import logging
import time
from datetime import datetime, timezone
from typing import List, Optional, Dict, Tuple

from application.model.action.action import Action
from application.model.action.action_set import ActionSet
from application.model.context.isolation_context import IsolationContext
from application.model.routine.advanced_tab_routine import AdvancedTabRoutine
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep
from application.model.state.isolation.isolation_state import IsolationState
from application.model.task import Task
from application.service.isolation_state_registry_service import IsolationStateRegistryService
from application.service.mcu_service import MCUService
from application.service.mcu_state_tracker_service import MCUStateTrackerService


class StateManager:
    """
    The StateManager tracks the current state of the system, which routines are available from that state, and has a
    queue for which routines to perform next. Also interacts with the MCUService to perform the routines.
    """

    def __init__(self, mcu_state_tracker_service: MCUStateTrackerService, mcu_service: MCUService,
                 isolation_state_registry_service: IsolationStateRegistryService, isolation_context: IsolationContext,
                 disable_routines_between: Tuple[str, str]):
        self.mcu_state_tracker_service = mcu_state_tracker_service
        self.mcu_service = mcu_service
        self.isolation_state_service = isolation_state_registry_service
        self.isolation_context = isolation_context
        self.disable_routines_between = disable_routines_between

        self.is_initialized = False
        self.task_queue: List[Task] = []
        self.lock_queue = False
        self.automated_routines_disabled = False
        self.running_routine = None

    def get_current_isolation_state(self) -> IsolationState:
        return self.isolation_context.get_state()

    @property
    def list_available_isolation_states(self) -> List[IsolationState]:
        return self.isolation_state_service.all_isolation_states()

    def change_isolation_state(self, new_state_name: str):

        logging.info(f"Changing isolation state from {self.get_current_isolation_state().name} to {new_state_name}")

        new_state = self.isolation_state_service.get_isolation_state(new_state_name)

        for routine in self.isolation_context.change_state(new_state):
            # Need to perform these right away rather than adding them to the queue
            self.perform_routine(routine)

    def initialize_isolation_state_context(self):
        """Function to initialize the isolation state context and perform any actions required during startup.
        """

        # Get the current actuator states of the system
        actual_actuator_states = self.mcu_state_tracker_service.get_actuator_states()

        logging.info(f"Initial actuator states: {actual_actuator_states}")

        # We always start up in the default state
        isolation_state_instance = self.isolation_state_service.get_isolation_state('DefaultState')
        self.isolation_context.state = isolation_state_instance

    @property
    def current_task_queue(self) -> List[Task]:
        return self.task_queue

    @property
    def currently_running_routine(self) -> Optional[Routine]:
        return self.running_routine

    def add_routine_to_queue(self,
                             routine: Routine,
                             isolation_state: Optional[IsolationState] = None,
                             to_start: bool = False):
        self.lock_queue = True
        task = Task(routine, isolation_state)
        if to_start:
            self.task_queue = [task] + self.task_queue
        else:
            self.task_queue.append(task)
        self.lock_queue = False

    def enable_automated_routine_running(self):
        logging.debug(f"Enabled running of new routines")
        self.automated_routines_disabled = False

    def disable_automated_routine_running(self):
        logging.debug(f"Disabled running of new routines, but will finish the current one if it is in progress and will"
                      f"finish a state transition if it is in progress")
        self.automated_routines_disabled = True

    @property
    def routines_currently_disabled(self):
        """Helper function to determine if routines are currently disabled based on the time"""

        from datetime import time as dtime

        local_timezone = datetime.now(timezone.utc).astimezone().tzinfo
        local_time = datetime.now(local_timezone).timetz()

        start_time = dtime.fromisoformat(self.disable_routines_between[0]).replace(tzinfo=local_timezone)
        end_time = dtime.fromisoformat(self.disable_routines_between[1]).replace(tzinfo=local_timezone)

        if start_time < end_time:
            return start_time <= local_time <= end_time
        else:
            # Timerange spans midnight
            return start_time <= local_time or local_time <= end_time

    def perform_next_routine_in_queue(self):
        if self.lock_queue:
            return

        if not self.task_queue:
            return

        # Not popping off the queue until we actually run it
        next_task = self.task_queue[0]

        if self.routines_currently_disabled and not isinstance(next_task.routine, AdvancedTabRoutine):
            logging.warning(f"Cannot run the {next_task.routine.name} routine because routine running is disabled "
                            f"between {self.disable_routines_between[0]} and {self.disable_routines_between[1]}; "
                            f"ignoring this task and removing it from the queue")
            _ = self.task_queue.pop(0)
            return

        # If we have disabled automated routine running, only run the AdvancedTabRoutines
        if self.automated_routines_disabled and not isinstance(next_task.routine, AdvancedTabRoutine):
            return

        # Similarly, if we have enabled automated routine running, do not run any AdvancedTabRoutines
        if not self.automated_routines_disabled and isinstance(next_task.routine, AdvancedTabRoutine):
            logging.warning(f"Cannot run AdvancedTabRoutine {next_task.routine} because automated routine running has "
                            f"not been disabled; ignoring this task and removing it from the queue")
            _ = self.task_queue.pop(0)
            return

        if next_task.isolation_state is not None and self.get_current_isolation_state() != next_task.isolation_state:
            self.change_isolation_state(next_task.isolation_state.name)

        # One more check in case the user disabled automated routine running while the system was changing state
        if self.automated_routines_disabled and not isinstance(next_task.routine, AdvancedTabRoutine):
            return

        # Now we're running this task, so pop it off the queue
        task = self.task_queue.pop(0)
        self.perform_routine(task.routine)

    def perform_action(self, action: Action):

        logging.debug(f"Performing action {action}")

        if action.set_to_value is None:
            # This is a sensor that needs to be read
            response = self.mcu_service.get_sensor_state(action.device_id)
        else:
            # This is an actuator to set
            response = self.mcu_service.set_actuator_state(action.device_id, action.set_to_value)

        self.mcu_state_tracker_service.update_tracked_state(response)

    def perform_routine_step(self, routine_step: RoutineStep):
        action_set = routine_step.action_set
        if action_set is not None:
            for action in action_set:

                self.perform_action(action)

        time.sleep(routine_step.then_wait_n_sec)

    def perform_routine(self, routine: Routine):

        if not isinstance(routine, AdvancedTabRoutine) and self.routines_currently_disabled:
            raise RuntimeError(f"Cannot run the {routine.name} routine because routine running is disabled between "
                               f"{self.disable_routines_between[0]} and {self.disable_routines_between[1]}")

        if self.running_routine is not None:
            raise RuntimeError(f"Cannot run the {routine.name} routine because the {self.running_routine.name} routine"
                               f"is already running")

        self.running_routine = routine

        try:

            logging.info(f"Performing routine {routine.name}")

            if not routine.can_run_in_state(self.get_current_isolation_state()):
                raise RuntimeError(f"Cannot run the {routine.name} routine from the "
                                   f"{self.get_current_isolation_state().name} state")

            for routine_step in routine:
                try:
                    self.perform_routine_step(routine_step)
                except RuntimeError as e:

                    logging.error(f"Encountered an error while performing routine {routine.name}; running failure "
                                  f"recovery steps")

                    # We encountered an error while performing the routine, so we need to run the failure recovery steps
                    for failure_recovery_step in routine.failure_recovery_steps:

                        logging.error(f"Performing actions {failure_recovery_step.action_set}")
                        try:
                            self.perform_routine_step(failure_recovery_step)
                        except:
                            # Even if we encounter an exception, we want to perform all the steps
                            pass

                    # Prevent any other routines from running until the user manually enables this on the advanced tab
                    self.disable_automated_routine_running()

                    raise e

        except Exception as e:

            raise e

        finally:

            self.running_routine = None

    # Manage state function is intended to be run as a looping thread. Should periodically monitor & control the recycler
    def manage_state(self):
        while True:

            if not self.is_initialized:
                logging.info(f"Initializing the state tracker and isolation context from the MCU")

                try:
                    system_snapshot = self.mcu_service.get_system_snapshot()
                except Exception as e:
                    # If the MCU isn't ready yet, it will sometimes raise an error
                    time.sleep(3)
                    continue

                self.mcu_state_tracker_service.update_tracked_state(system_snapshot)
                self.initialize_isolation_state_context()

                # We should always start at the default state
                # TODO - in the future, may want to remove this so it can continue operating through restarts gracefully
                if self.get_current_isolation_state().name != 'DefaultState':
                    self.change_isolation_state('DefaultState')

                self.is_initialized = True

            self.perform_next_routine_in_queue()

            time.sleep(1)
