from application.controller.schema.utils import get_schema_from_file


class Measurements:

    @staticmethod
    def get_schema():
        return get_schema_from_file('measurement.json')

    def __init__(self, measurements):
        self.measurements = measurements
