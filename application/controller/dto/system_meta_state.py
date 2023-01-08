class SystemMetaState:

    @staticmethod
    def get_schema():
        return {
            "type": "object",
            "properties": {
                "disable_automated_routines": {"type": "boolean"}
                }
            }

    def __init__(self, disable_automated_routines: bool):
        self.disable_automated_routines = disable_automated_routines
