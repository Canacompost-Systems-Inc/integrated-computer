class MachineState:

    @staticmethod
    def get_schema():
        return {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                    "actuators": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "id": {"type": "string"},
                                "type": {"type": "string"},
                                "description": {"type": "string"},
                                "value": {"type": "string"},
                                "options": {
                                    "type": "array",
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
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "shared_air":{
                                "type": "object",
                                "additionalProperties": False,
                                "properties": {
                                    "pressure":{"type": ["number", "null"]}
                                }
                            },
                            "shredder":{
                                "type": "object",
                                "additionalProperties": False,
                                "properties": {
                                    "humidity":{"type": ["number", "null"]},
                                    "c02":{"type": ["number", "null"]},
                                    "air_temperature":{"type": ["number", "null"]},
                                    "soil_temperature":{"type": ["number", "null"]}
                                }
                            },
                            "bioreactor_1":{
                                "type": "object",
                                "additionalProperties": False,
                                "properties": {
                                    "humidity":{"type": ["number", "null"]},
                                    "c02":{"type": ["number", "null"]},
                                    "air_temperature":{"type": ["number", "null"]},
                                    "soil_temperature":{"type": ["number", "null"]}
                                }
                            },
                            "bioreactor_2":{
                                "type": "object",
                                "additionalProperties": False,
                                "properties": {
                                    "humidity":{"type": ["number", "null"]},
                                    "c02":{"type": ["number", "null"]},
                                    "air_temperature":{"type": ["number", "null"]},
                                    "soil_temperature":{"type": ["number", "null"]}
                                }
                            },
                            "bsf_reproduction":{
                                "type": "object",
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