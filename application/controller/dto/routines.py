from application.controller.schema.utils import get_schema_from_file


class Routines:

    @staticmethod
    def get_schema():
        return get_schema_from_file('routine.json')

    def __init__(self, routines):
        self.routines = routines
