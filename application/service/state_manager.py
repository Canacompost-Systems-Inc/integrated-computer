import logging
import time
from typing import List, Optional, Dict

from application.model.action.action import Action
from application.model.action.action_set import ActionSet
from application.model.context.isolation_context import IsolationContext
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
                 isolation_state_registry_service: IsolationStateRegistryService, isolation_context: IsolationContext):
        self.mcu_state_tracker_service = mcu_state_tracker_service
        self.mcu_service = mcu_service
        self.isolation_state_service = isolation_state_registry_service
        self.isolation_context = isolation_context

        self.is_initialized = False
        self.task_queue: List[Task] = []
        self.lock_queue = False
        self.disable_automated_routines = False
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
        """Function used during initialization to determine the isolation state based on the current state reported by
        the MCU, and then to set the isolation state context based on this.
        """

        def get_expected_actuator_states(_isolation_state: IsolationState) -> Dict[str, str]:
            """Use the isolation_state.activate_state function to determine the expected actuator states for a given
            isolation state.
            """
            actuator_states = {}

            routine: Routine = _isolation_state.activate_state()

            for routine_step in routine:
                action_set = routine_step.action_set
                if action_set is not None:
                    for action in action_set:

                        if action.set_to_value is not None:
                            # This is an actuator to set
                            actuator_states[action.device_id] = action.set_to_value

            return actuator_states

        def all_expected_actuator_states_are_set(
                actual_states: Dict[str, str],
                expected_states: Dict[str, str]) -> bool:

            return all([
                expected_value == actual_states[device_id]
                for device_id, expected_value
                in expected_states.items()
            ])

        # Get the current actuator states of the system
        actual_actuator_states = self.mcu_state_tracker_service.get_actuator_states()

        logging.info(f"Initial actuator states: {actual_actuator_states}")

        # Get the expected actuator states under each isolation state
        expected_actuator_states = {}
        for isolation_state in self.list_available_isolation_states:

            expected_actuator_states[isolation_state.name] = get_expected_actuator_states(isolation_state)

        # Determine which isolation_state is currently set - raise error if more than one matches
        matching_isolation_states = []
        for isolation_state_name in expected_actuator_states:

            if all_expected_actuator_states_are_set(actual_actuator_states, expected_actuator_states[isolation_state_name]):
                matching_isolation_states.append(isolation_state_name)

        if len(matching_isolation_states) == 0:
            raise RuntimeError(f"MCU is reporting actuator states that do not match any isolation states")

        elif len(matching_isolation_states) > 1:
            raise RuntimeError(f"MCU is reporting actuator states that match multiple isolation states: {matching_isolation_states}")

        # Set the isolation_context object to the right state
        isolation_state_name = matching_isolation_states[0]
        isolation_state_instance = self.isolation_state_service.get_isolation_state(isolation_state_name)
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
        self.disable_automated_routines = False

    def disable_automated_routine_running(self):
        self.disable_automated_routines = True

    def perform_next_routine_in_queue(self):
        if self.lock_queue:
            return

        if not self.task_queue:
            return

        task = self.task_queue.pop(0)

        if task.isolation_state is not None and self.get_current_isolation_state() != task.isolation_state:
            self.change_isolation_state(task.isolation_state.name)

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

                    # TODO - we should also prevent any other routines from running until the user can manually unlock this (to add when we have api to lock the routines)

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

            if not self.disable_automated_routines:
                self.perform_next_routine_in_queue()
            else:
                logging.debug(f"Not performing routines because automated routine running is disabled")

            time.sleep(3)
