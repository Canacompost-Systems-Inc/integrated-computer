import logging
import time
from dataclasses import dataclass
from typing import List, Optional, Dict

from application.model.context.isolation_context import IsolationContext
from application.model.routine.routine import Routine
from application.model.state.isolation.isolation_state import IsolationState
from application.service.isolation_state_registry_service import IsolationStateRegistryService
from application.service.routine_registry_service import RoutineRegistryService
from application.service.mcu_service import MCUService
from application.service.mcu_state_tracker_service import MCUStateTrackerService


@dataclass
class Task:
    """Class for performing a routine in a particular isolation state"""
    routine: Routine
    isolation_state: Optional[IsolationState] = None


class StateManager:
    """
    The StateManager tracks the current state of the system, which routines are available from that state, and has a
    queue for which routines to perform next. Also interacts with the MCUService to perform the routines.
    """

    def __init__(self, mcu_state_tracker_service: MCUStateTrackerService, routines_service: RoutineRegistryService,
                 mcu_service: MCUService, isolation_state_registry_service: IsolationStateRegistryService,
                 isolation_context: IsolationContext):
        self.mcu_state_tracker_service = mcu_state_tracker_service
        self.routines_service = routines_service
        self.mcu_service = mcu_service
        self.isolation_state_service = isolation_state_registry_service
        self.isolation_context = isolation_context

        self.is_initialized = False
        self.task_queue: List[Task] = []

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
            raise RuntimeError(f"MCU is reporting actuator states that match multiple isolation states")

        # Set the isolation_context object to the right state
        isolation_state_name = matching_isolation_states[0]
        isolation_state_instance = self.isolation_state_service.get_isolation_state(isolation_state_name)
        self.isolation_context.state = isolation_state_instance

    @property
    def current_task_queue(self) -> List[Task]:
        return self.task_queue

    def add_routine_to_queue(self, routine: Routine, isolation_state: Optional[IsolationState] = None):
        self.task_queue.append(Task(routine, isolation_state))

    def perform_next_routine_in_queue(self):
        if not self.task_queue:
            return

        task = self.task_queue.pop(0)

        if task.isolation_state is not None and self.get_current_isolation_state() != task.isolation_state:
            self.change_isolation_state(task.isolation_state.name)

        self.perform_routine(task.routine)

    def perform_routine(self, routine: Routine):

        logging.info(f"Performing routine {routine.name}")

        if not routine.can_run_in_state(self.get_current_isolation_state()):
            raise RuntimeError(f"Cannot run the {routine.name} routine from the "
                               f"{self.get_current_isolation_state().name} state")

        for routine_step in routine:
            action_set = routine_step.action_set
            if action_set is not None:
                for action in action_set:

                    logging.debug(f"Performing action {action}")

                    if action.set_to_value is None:
                        # This is a sensor that needs to be read
                        response = self.mcu_service.get_sensor_state(action.device_id)
                    else:
                        # This is an actuator to set
                        response = self.mcu_service.set_actuator_state(action.device_id, action.set_to_value)

                    self.mcu_state_tracker_service.update_tracked_state(response)

            # TODO - commenting out for testing, uncomment before merging
            time.sleep(routine_step.duration_sec / 4)
            # time.sleep(routine_step.duration_sec)

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

                # TODO - remove this once testing is done (setting these so the mcu state tracker service has values
                routine = self.routines_service.get_routine('ReadSensorsBioreactor1Routine')
                isolation_state = self.isolation_state_service.get_isolation_state('AirLoopBioreactor1State')
                self.add_routine_to_queue(routine, isolation_state)

            self.perform_next_routine_in_queue()




            # latest_actuator_state = self.mcu_state_tracker_service.get_actuator_states()
            # logging.warning(f"latest_actuator_state: {latest_actuator_state}")
            #
            # latest_measurements = self.mcu_state_tracker_service.get_latest_measurements()
            # logging.warning(f"latest_measurements: {latest_measurements}")
            #
            # if self.get_current_isolation_state().name != 'AirLoopBioreactor1State':
            #     self.change_isolation_state('AirLoopBioreactor1State')
            #
            #     routine = self.routines_service.get_routine('ReadSensorsBioreactor1Routine')
            #     isolation_state = self.isolation_state_service.get_isolation_state('AirLoopBioreactor1State')
            #     self.add_routine_to_queue(routine, isolation_state)


            # import random
            # if random.random() < 0.50:
            #     possible_states = [s.name for s in self.list_available_isolation_states if s.name != self.current_isolation_state.name and s.name != 'InitialState']
            #     chosen_state = random.choice(possible_states) if self.current_isolation_state.name == 'DefaultState' else 'DefaultState'
            #     print(f"chosen_state: {chosen_state}")
            #     self.change_isolation_state(chosen_state)

            time.sleep(3)


            # NOTE - leaving test code in until we write the new management service

            # print("########## Testing get system snapshot endpoint ##########")
            # measurement_map = self.mcu_service.get_system_snapshot()
            # print(f"measurement_map: {measurement_map}")

            # print("########## Testing set actuator state endpoint ##########")
            #
            # def get_number_of_possible_states(device_id):
            #     device = self.mcu_service.device_map[device_id]
            #     return len(device.possible_states)
            #
            # def set_to_next_state(device_id, current_measurement_map):
            #     device = self.mcu_service.device_map[device_id]
            #     current_state = current_measurement_map[device.location][device.device_id][1][0].val
            #
            #     # Get the next possible state
            #     possible_states = list(device.possible_states.keys())
            #     possible_states = possible_states + possible_states
            #     new_state = possible_states[possible_states.index(current_state) + 1]
            #
            #     print(f"Setting state of {device.device_friendly_name} from {current_state} to {new_state}")
            #     return self.mcu_service.set_actuator_state(actuator_device_id=device_id, value=new_state)
            #
            # cur_measurement_map = measurement_map
            # for location in measurement_map:
            #     for device_id in measurement_map[location]:
            #
            #         if self.mcu_service.device_map[device_id].device_category != 'actuator':
            #             continue
            #
            #         for i in range(get_number_of_possible_states(device_id)):
            #
            #             time.sleep(3)
            #
            #             update_to_measurement_map = set_to_next_state(device_id, cur_measurement_map)
            #
            #             for loc in update_to_measurement_map:
            #                 for did in update_to_measurement_map[loc]:
            #                     cur_measurement_map[loc][did] = update_to_measurement_map[loc][did]
            #
            #             print(f"measurement_map: {cur_measurement_map}")



            # # Testing set actuator state endpoint
            # print("########## Testing set actuator state endpoint ##########")
            # import random
            # set_state = random.random() > 0.5
            # if set_state:
            #     print(f"measurement_map: {measurement_map}")
            #     current_state = measurement_map['BIOREACTOR1']['e1'][1][0].val
            #     new_state = None
            #     device = self.mcu_service.device_map['e1']
            #     for k, v in device.possible_states.items():
            #         if k != current_state:
            #             new_state = k
            #             break
            #
            #     print(f"Setting state of {device.device_friendly_name} from {current_state} to {new_state}")
            #     measurement_map = self.mcu_service.set_actuator_state(actuator_device_id='e0', value=new_state)
            #     print(f"measurement_map: {measurement_map}")
            #
            # # Testing get sensor state endpoint
            # print("########## Testing get sensor state endpoint ##########")
            # measurement_map = self.mcu_service.get_sensor_state(sensor_device_id='c0')
            # print(f"measurement_map: {measurement_map}")
            #
            # # Testing get actuator state endpoint
            # print("########## Testing get actuator state endpoint ##########")
            # measurement_map = self.mcu_service.get_actuator_state(actuator_device_id='e0')
            # print(f"measurement_map: {measurement_map}")
