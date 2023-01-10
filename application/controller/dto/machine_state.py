from application.controller.schema.utils import get_schema_from_file


class MachineState:

    @staticmethod
    def get_schema():
        return get_schema_from_file('state.json')

    def __init__(self, actuators, sensors):
        self.actuators = actuators
        self.sensors = sensors
