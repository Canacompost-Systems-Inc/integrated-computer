import time

class StateManager():
    """
    The StateManager keeps track of the recycler
    """

    def __init__(self, oxygen_effector, temperature_effector):
        self.oxygen_effector = oxygen_effector
        self.temperature_effector = temperature_effector

        self.effectors = [
            self.oxygen_effector,
            self.temperature_effector]

    # Manage state function is intended to be run as a looping thread. Should periodically monitor & control the recycler
    def manage_state(self):
        while True:
            print("Monitoring and controlling the recycler!")
            time.sleep(3)