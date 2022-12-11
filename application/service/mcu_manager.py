import time

class StateManager():
    """
    The StateManager keeps track of the recycler
    """

    def __init__(self, routines_service, mcu_service):
        self.routines_service = routines_service
        self.mcu_service = mcu_service

    # Manage state function is intended to be run as a looping thread. Should periodically monitor & control the recycler
    def manage_state(self):
        while True:

            time.sleep(3)

            # NOTE - leaving test code in until we write the new management service

            print("########## Testing get system snapshot endpoint ##########")
            measurement_map = self.mcu_service.get_system_snapshot()
            print(f"measurement_map: {measurement_map}")

            print("########## Testing set actuator state endpoint ##########")

            def get_number_of_possible_states(device_id):
                device = self.mcu_service.device_map[device_id]
                return len(device.possible_states)

            def set_to_next_state(device_id, current_measurement_map):
                device = self.mcu_service.device_map[device_id]
                current_state = current_measurement_map[device.location][device.device_id][1][0].val

                # Get the next possible state
                possible_states = list(device.possible_states.keys())
                possible_states = possible_states + possible_states
                new_state = possible_states[possible_states.index(current_state) + 1]

                print(f"Setting state of {device.device_friendly_name} ({device_id}) from {current_state} to {new_state}")
                return self.mcu_service.set_actuator_state(actuator_device_id=device_id, value=new_state)

            cur_measurement_map = measurement_map
            for location in measurement_map:
                for device_id in measurement_map[location]:

                    if device_id in ['e0', 'e1', 'e2', 'e7', 'e8', 'e9', 'ea', 'eb', 'ed']:
                        continue

                    if self.mcu_service.device_map[device_id].device_category != 'actuator':
                        continue

                    for i in range(get_number_of_possible_states(device_id)):

                        time.sleep(3)

                        update_to_measurement_map = set_to_next_state(device_id, cur_measurement_map)

                        for loc in update_to_measurement_map:
                            for did in update_to_measurement_map[loc]:
                                cur_measurement_map[loc][did] = update_to_measurement_map[loc][did]

                        # print(f"measurement_map: {cur_measurement_map}")

                    break
                break




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
