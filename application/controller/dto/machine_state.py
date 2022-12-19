class MachineState:

    @staticmethod
    def get_schema():
        return {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                    "actuators": {
                        "type": ["array", "null"],
                        "items": {
                            "type": ["object", "null"],
                            "additionalProperties": False,
                            "properties": {
                                "id": {"type": "string"},
                                "type": {"type": "string"},
                                "description": {"type": "string"},
                                "value": {"type": "string"},
                                "options": {
                                    "type": ["array", "null"],
                                    "additionalProperties": False,
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "name": {"type": "string"},
                                            "value": {"type": "number"}
                                        },
                                        "required": ["name", "value"]
                                    }
                                },
                                "min": {"type": ["number", "null"]}, 
                                "max": {"type": ["number", "null"]},
                                "step": {"type": ["number", "null"]},
                                "unit": {"type": ["string", "null"]}
                            },
                            "required": ["id", "type", "description", "value"]
                        }
                    },
                    "sensors":{
                        "type": ["object", "null"],
                        "additionalProperties": False,
                        "properties": {
                            "shared_air":{
                                "type": ["object", "null"],
                                "additionalProperties": False,
                                "properties": {
                                    "pressure":{"type": ["number", "null"]}
                                }
                            },
                            "shredder":{
                                "type": ["object", "null"],
                                "additionalProperties": False,
                                "properties": {
                                    "humidity":{"type": ["number", "null"]},
                                    "c02":{"type": ["number", "null"]},
                                    "air_temperature":{"type": ["number", "null"]},
                                    "soil_temperature":{"type": ["number", "null"]}
                                }
                            },
                            "bioreactor_1":{
                                "type": ["object", "null"],
                                "additionalProperties": False,
                                "properties": {
                                    "humidity":{"type": ["number", "null"]},
                                    "c02":{"type": ["number", "null"]},
                                    "air_temperature":{"type": ["number", "null"]},
                                    "soil_temperature":{"type": ["number", "null"]}
                                }
                            },
                            "bioreactor_2":{
                                "type": ["object", "null"],
                                "additionalProperties": False,
                                "properties": {
                                    "humidity":{"type": ["number", "null"]},
                                    "c02":{"type": ["number", "null"]},
                                    "air_temperature":{"type": ["number", "null"]},
                                    "soil_temperature":{"type": ["number", "null"]}
                                }
                            },
                            "bsf_reproduction":{
                                "type": ["object", "null"],
                                "additionalProperties": False,
                                "properties": {
                                    "humidity":{"type": ["number", "null"]},
                                    "c02":{"type": ["number", "null"]},
                                    "air_temperature":{"type": ["number", "null"]},
                                    "soil_temperature":{"type": ["number", "null"]}
                                }
                            }
                        }
                    }
                }
            }

    def __init__(self, actuators, sensors):
        self.actuators = actuators
        self.sensors = sensors