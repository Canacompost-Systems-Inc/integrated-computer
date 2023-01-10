from application.controller.schema.utils import get_schema_from_file


class SystemMetaState:

    @staticmethod
    def get_schema():
        return get_schema_from_file('meta_state.json')

    def __init__(self, disable_automated_routines: bool):
        self.disable_automated_routines = disable_automated_routines
