class Routines:

    @staticmethod
    def get_schema():
        return {
            "type": "object",
            "properties": {
                "routines": {
                    "type": ["array", "null"],
                    "items": {
                        "type": ["object", "null"],
                        "properties": {
                            "name": {"type": "string"}
                        },
                        "required": ["name"]
                    }
                }
            }
        }

    def __init__(self, routines):
        self.routines = routines
