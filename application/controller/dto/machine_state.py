class MachineState:
    
    @staticmethod
    def get_schema():
        return {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "actuators":{
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "shared_air":{
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "rotary_valve_1":{"type": "number"},
                                "rotary_valve_2":{"type": "number"},
                                "rotary_valve_3":{"type": "number"},
                                "discrete_valve_1":{"type": "number"},
                                "discrete_valve_2":{"type": "number"},
                                "discrete_valve_3":{"type": "number"},
                                "flap_valve_1":{"type": "boolean"},
                                "flap_valve_2":{"type": "boolean"},
                                "flap_valve_3":{"type": "boolean"},
                                "blower_on":{"type": "boolean"},
                                "o3_generator":{"type": "boolean"},
                                "blower_strength":{"type": "number"}
                            }
                        },
                        "shredder":{
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "out_valve":{"type": "boolean"},
                                "in_valve":{"type": "boolean"}
                            }
                        },
                        "bioreactor_1":{
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "out_valve":{"type": "boolean"},
                                "in_valve":{"type": "boolean"}
                            }
                        },
                        "bioreactor_2":{
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "out_valve":{"type": "boolean"},
                                "in_valve":{"type": "boolean"}
                            }
                        },
                        "bsf_reproduction":{
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "out_valve":{"type": "boolean"},
                                "in_valve":{"type": "boolean"},
                                "light": {"type": "boolean"}
                            }
                        }
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


