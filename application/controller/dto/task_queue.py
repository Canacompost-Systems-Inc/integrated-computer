class TaskQueue:

    @staticmethod
    def get_schema():
        return {
            "type": "object",
            "properties": {
                "currently_running_routine": {
                    "type": ["object", "null"],
                    "properties": {
                        "name": {"type": "string"}
                    }
                },
                "tasks": {
                    "type": ["array", "null"],
                    "items": {
                        "type": ["object", "null"],
                        "properties": {
                            "routine": {
                                "type": ["object", "null"],
                                "properties": {
                                    "name": {"type": "string"}
                                },
                                "required": ["name"]
                            }
                        }
                    }
                }
            }
        }

    def __init__(self, currently_running_routine, tasks):
        self.currently_running_routine = currently_running_routine
        self.tasks = tasks
