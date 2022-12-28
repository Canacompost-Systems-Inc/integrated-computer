import time
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Optional

from application.model.context.isolation_context import IsolationContext
from application.model.routine.routine import Routine
from application.model.state.isolation.isolation_state import IsolationState
from application.service.isolation_state_registry_service import IsolationStateRegistryService
from application.service.routine_registry_service import RoutineRegistryService
from application.service.mcu_service import MCUService


# TODO:
# 1. Add function for determining which state the system is currently in based on the system snapshot

# 2. Have the manage state function get the system snapshot and set the isolation_state if it is not already set (for startup)

# 3. Add in logic for keeping track of the current system state, and updating it with the latest readings
#     - this includes the get_sensor_state etc. endpoints which are currently not being handled

# 3. Add Routines
# 	- MoveCompostToBioreactor1
# 	- MoveCompostToBioreactor2
# 	- MoveCompostToBSFReproduction
# 	- MoveCompostToSieve
#
# 	- CoolAndDehumidify SS B1 B2 BSF S (i.e. run through dehumidifier)
# 	- Humidify SS B1 B2 BSF S (i.e. activate water pump)
# 	- Heat SS B1 B2 BSF S (i.e. activate heater)
# 	- ReadSensors SS B1 B2 BSF S
#
# 4. Make note about needing a concept of 'continuous tasks' like checking the flow rate and the o3 sensor regularly
#
# 5. StateManager
# 	- In ManageState thread, will check which readings haven't been done in a while and will add these to the task queue (i.e. will add ReadSensors and then will call a function to check if any measurements are out of bounds, and if so will have logic for how to handle these - that is, will know which routines to add to the queue in these cases)
# 	- Can have a config value which tells it how long to wait between sampling containers
# 	- nvm, this logic belongs in the CompostManager
#
# 	- This structure handles cooling and dehumidifying, humidifying, heating, and reading sensors; but it does not cover moving compost from one stage to the next
# 		- Maybe StateManager has functions for adding the movement of compost to the queue (or a more general function that could be used by the UI as well?), and the logic for when to do this can be handled by the automation layer (CompostManager?)
#
# 6. Add this to the description of the action or ActionSet:
#
#
# This registers each low-level action that the system can perform. Routines will be sets of actions with timing and
#     dependencies (e.g. which bioreactor needs to be active in the shared air). The goal is to make routines consist
#     of a set of logical steps so that they are readily understandable.
#
#     There may be a better way to organize this, perhaps by creating a model for each action, and just registering them
#     here. But that can be handled in a refactor later. For now, we'll have a set of functions here that represent the
#     discrete actions that the system can take.
#
# 7. Later can add in test code that will replace the MCU so that when the commands are written to it, it responds correctly (and thus it keeps track of the current state of the system, and assumes the default states when it starts up)


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

    def __init__(self, routines_service: RoutineRegistryService, mcu_service: MCUService,
                 isolation_state_registry_service: IsolationStateRegistryService, isolation_context: IsolationContext):
        self.routines_service = routines_service
        self.mcu_service = mcu_service
        self.isolation_state_service = isolation_state_registry_service
        #
        # self.available_routines = defaultdict(list)
        # for state in self.isolation_state_service.isolation_state_map.values():
        #     for routine_name, routine in self.routines_service.routine_map.items():
        #         if routine.can_run_in_state(state):
        #             self.available_routines[state.name].append(routine_name)

        self.isolation_context = isolation_context

        self.task_queue: List[Task] = []

    @property
    def current_isolation_state(self) -> IsolationState:
        return self.isolation_context.state

    @property
    def available_isolation_states(self) -> List[IsolationState]:
        return self.isolation_state_service.isolation_state_map.values()

    def change_isolation_state(self, new_state: IsolationState):
        for routine in self.isolation_context.change_state(new_state):
            # Need to perform these right away rather than adding them to the queue
            self.perform_routine(routine)

    @property
    def current_task_queue(self) -> List[Task]:
        return self.task_queue

    def add_routine_to_queue(self, routine: Routine, isolation_state: Optional[IsolationState] = None):
        self.task_queue.append(Task(routine, isolation_state))

    def perform_next_routine_in_queue(self):
        if not self.task_queue:
            return

        task = self.task_queue.pop(0)

        if self.current_isolation_state != task.isolation_state:
            self.change_isolation_state(task.isolation_state)

        self.perform_routine(task.routine)

    def perform_routine(self, routine: Routine):

        if not routine.can_run_in_state(self.current_isolation_state):
            raise RuntimeError(f"Cannot run the {routine.name} routine from the {self.current_isolation_state.name} state")

        for routine_step in routine:
            action_set = routine_step.action_set
            if action_set is not None:
                for action in action_set:

                    if action.set_to_value is None:
                        # This is a sensor that needs to be read
                        self.mcu_service.get_sensor_state(action.device_id)
                    else:
                        # This is an actuator to set
                        self.mcu_service.set_actuator_state(action.device_id, action.set_to_value)

            time.sleep(routine_step.duration_sec)

    # Manage state function is intended to be run as a looping thread. Should periodically monitor & control the recycler
    def manage_state(self):
        while True:

            # TODO - requeue items with the PriorityService, when available
            # self.task_queue = self.priority_service.reprioritize_task_queue(self.task_queue)

            self.perform_next_routine_in_queue()

            time.sleep(3)

            # NOTE - leaving test code in until we write the new management service

            print("########## Testing get system snapshot endpoint ##########")
            measurement_map = self.mcu_service.get_system_snapshot()
            print(f"measurement_map: {measurement_map}")

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
