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
                                "min": {"type": "number"},
                                "max": {"type": "number"},
                                "step": {"type": "number"},
                                "unit": {"type": "string"}
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
                                    "pressure":{"type": "number"}
                                }
                            },
                            "shredder":{
                                "type": "object",
                                "additionalProperties": False,
                                "properties": {
                                    "humidity":{"type": "number"},
                                    "c02":{"type": "number"},
                                    "air_temperature":{"type": "number"},
                                    "soil_temperature":{"type": "number"}
                                }
                            },
                            "bioreactor_1":{
                                "type": "object",
                                "additionalProperties": False,
                                "properties": {
                                    "humidity":{"type": "number"},
                                    "c02":{"type": "number"},
                                    "air_temperature":{"type": "number"},
                                    "soil_temperature":{"type": "number"}
                                }
                            },
                            "bioreactor_2":{
                                "type": "object",
                                "additionalProperties": False,
                                "properties": {
                                    "humidity":{"type": "number"},
                                    "c02":{"type": "number"},
                                    "air_temperature":{"type": "number"},
                                    "soil_temperature":{"type": "number"}
                                }
                            },
                            "bsf_reproduction":{
                                "type": "object",
                                "additionalProperties": False,
                                "properties": {
                                    "humidity":{"type": "number"},
                                    "c02":{"type": "number"},
                                    "air_temperature":{"type": "number"},
                                    "soil_temperature":{"type": "number"}
                                }
                            }
                        }
                    }
                }
            }

    def __init__(self, actuators, sensors):
        self.actuators = actuators
        self.sensors = sensors