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
