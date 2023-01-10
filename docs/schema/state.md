# State Schema

Used to get the current actuator state and sensor measurements, and to set the actuator state and set points for the sensor measurements. Supports GET and POST.

### JSON Schema

```json
{
    "type": "object",
    "properties": {
        "actuators": {
            "type": ["array", "null"],
            "items": {
                "type": ["object", "null"],
                "properties": {
                    "id": {"type": "string"},
                    "type": {"type": "string"},
                    "description": {"type": "string"},
                    "value": {"type": "string"},
                    "options": {
                        "type": ["array", "null"],
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
            "properties": {
                "shared_air":{
                    "type": ["object", "null"],
                    "properties": {
                        "flowrate":{"type": ["number", "null"]},
                        "o3":{"type": ["number", "null"]}
                    }
                },
                "shredder":{
                    "type": ["object", "null"],
                    "properties": {
                        "temperature":{"type": ["number", "null"]},
                        "humidity":{"type": ["number", "null"]},
                        "co2":{"type": ["number", "null"]},
                        "pressure":{"type": ["number", "null"]},
                        "h2":{"type": ["number", "null"]}
                    }
                },
                "bioreactor_1":{
                    "type": ["object", "null"],
                    "properties": {
                        "temperature":{"type": ["number", "null"]},
                        "humidity":{"type": ["number", "null"]},
                        "co2":{"type": ["number", "null"]},
                        "pressure":{"type": ["number", "null"]},
                        "h2":{"type": ["number", "null"]}
                    }
                },
                "bioreactor_2":{
                    "type": ["object", "null"],
                    "properties": {
                        "temperature":{"type": ["number", "null"]},
                        "humidity":{"type": ["number", "null"]},
                        "co2":{"type": ["number", "null"]},
                        "pressure":{"type": ["number", "null"]},
                        "h2":{"type": ["number", "null"]}
                    }
                },
                "bsf_reproduction":{
                    "type": ["object", "null"],
                    "properties": {
                        "temperature":{"type": ["number", "null"]},
                        "humidity":{"type": ["number", "null"]},
                        "co2":{"type": ["number", "null"]},
                        "pressure":{"type": ["number", "null"]},
                        "h2":{"type": ["number", "null"]}
                    }
                }
            }
        }
    }
}
```

### Examples

```console
user@local:~$ curl -X GET http://127.0.0.1:5000/state -H 'Content-Type: application/json' | python -m json.tool
{
    "py/object": "application.controller.dto.machine_state.MachineState",
    "actuators": [
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "e0",
            "type": "RADIO",
            "description": "Rotary Diverter Valve From Air Loop",
            "value": "1",
            "options": [
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "0",
                    "value": 0
                },
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "1",
                    "value": 1
                },
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "2",
                    "value": 2
                },
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "3",
                    "value": 3
                },
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "4",
                    "value": 4
                },
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "5",
                    "value": 5
                }
            ],
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "e1",
            "type": "RADIO",
            "description": "Rotary Diverter Valve To Air Loop",
            "value": "4",
            "options": [
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "0",
                    "value": 0
                },
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "1",
                    "value": 1
                },
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "2",
                    "value": 2
                },
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "3",
                    "value": 3
                },
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "4",
                    "value": 4
                },
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "5",
                    "value": 5
                }
            ],
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "e2",
            "type": "RADIO",
            "description": "Rotary Diverter Valve Compost Loop",
            "value": "1",
            "options": [
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "0",
                    "value": 0
                },
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "1",
                    "value": 1
                },
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "2",
                    "value": 2
                },
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "3",
                    "value": 3
                },
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "4",
                    "value": 4
                },
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "5",
                    "value": 5
                }
            ],
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "e3",
            "type": "SWITCH",
            "description": "Butterfly Valve From Shredder Storage",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "e4",
            "type": "SWITCH",
            "description": "Butterfly Valve From Bioreactor1",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "e5",
            "type": "SWITCH",
            "description": "Butterfly Valve From Bioreactor2",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "e6",
            "type": "SWITCH",
            "description": "Butterfly Valve From BSFReproduction",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "e7",
            "type": "SWITCH",
            "description": "Flap Diverter Valve Sensor Loop Bypass",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "e8",
            "type": "SWITCH",
            "description": "Flap Diverter Valve Radiator Bypass",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "eb",
            "type": "RANGE",
            "description": "Environment Exchange Out",
            "value": "0",
            "options": null,
            "min": 0,
            "max": 100,
            "step": 5,
            "unit": "percent"
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "ec",
            "type": "RANGE",
            "description": "Environment Exchange In",
            "value": "0",
            "options": null,
            "min": 0,
            "max": 100,
            "step": 5,
            "unit": "percent"
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "f0",
            "type": "SWITCH",
            "description": "Air Hammer BSFReproduction",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "e9",
            "type": "SWITCH",
            "description": "Water Pump Relay BSFReproduction",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "f6",
            "type": "SWITCH",
            "description": "Water Pump Relay Shredder Storage",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "f8",
            "type": "SWITCH",
            "description": "Water Pump Relay Bioreactor1",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "fa",
            "type": "SWITCH",
            "description": "Water Pump Relay Bioreactor2",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "f1",
            "type": "SWITCH",
            "description": "Regen Blower",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "f2",
            "type": "SWITCH",
            "description": "BSFReproduction Light",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "f3",
            "type": "SWITCH",
            "description": "Ozone Generator",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "f4",
            "type": "SWITCH",
            "description": "UVC Light",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        }
    ],
    "sensors": {
        "py/object": "application.controller.dto.machine_sensors.Sensors",
        "shared_air": {
            "py/object": "application.controller.dto.sensors.shared_air_sensors.SharedAirSensors",
            "flowrate": 19.88,
            "o3": 29.7
        },
        "shredder": {
            "py/object": "application.controller.dto.sensors.shredder_sensors.ShredderSensors",
            "temperature": null,
            "humidity": null,
            "co2": null,
            "pressure": null,
            "h2": null
        },
        "bioreactor_1": {
            "py/object": "application.controller.dto.sensors.bioreactor_1_sensors.Bioreactor1Sensors",
            "temperature": 27.62,
            "humidity": 45.88,
            "co2": 24.72,
            "pressure": 1.63,
            "h2": null
        },
        "bioreactor_2": {
            "py/object": "application.controller.dto.sensors.bioreactor_2_sensors.Bioreactor2Sensors",
            "temperature": null,
            "humidity": null,
            "co2": null,
            "pressure": null,
            "h2": null
        },
        "bsf_reproduction": {
            "py/object": "application.controller.dto.sensors.bsf_reproduction_sensors.BSFReproductionSensors",
            "temperature": null,
            "humidity": null,
            "co2": null,
            "pressure": null,
            "h2": null
        }
    }
}

user@local:~$ curl -X POST http://127.0.0.1:5000/state -H 'Content-Type: application/json' -d '{
    "py/object": "application.controller.dto.machine_state.MachineState",
    "actuators": [
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "e0",
            "type": "RADIO",
            "description": "Rotary Diverter Valve From Air Loop",
            "value": "4",
            "options": [
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "0",
                    "value": 0
                },
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "1",
                    "value": 1
                },
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "2",
                    "value": 2
                },
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "3",
                    "value": 3
                },
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "4",
                    "value": 4
                },
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "5",
                    "value": 5
                }
            ],
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "e1",
            "type": "RADIO",
            "description": "Rotary Diverter Valve To Air Loop",
            "value": "3",
            "options": [
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "0",
                    "value": 0
                },
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "1",
                    "value": 1
                },
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "2",
                    "value": 2
                },
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "3",
                    "value": 3
                },
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "4",
                    "value": 4
                },
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "5",
                    "value": 5
                }
            ],
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "e2",
            "type": "RADIO",
            "description": "Rotary Diverter Valve Compost Loop",
            "value": "1",
            "options": [
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "0",
                    "value": 0
                },
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "1",
                    "value": 1
                },
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "2",
                    "value": 2
                },
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "3",
                    "value": 3
                },
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "4",
                    "value": 4
                },
                {
                    "py/object": "application.controller.dto.actuators.options.Options",
                    "name": "5",
                    "value": 5
                }
            ],
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "e3",
            "type": "SWITCH",
            "description": "Butterfly Valve From Shredder Storage",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "e4",
            "type": "SWITCH",
            "description": "Butterfly Valve From Bioreactor1",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "e5",
            "type": "SWITCH",
            "description": "Butterfly Valve From Bioreactor2",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "e6",
            "type": "SWITCH",
            "description": "Butterfly Valve From BSFReproduction",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "e7",
            "type": "SWITCH",
            "description": "Flap Diverter Valve Sensor Loop Bypass",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "e8",
            "type": "SWITCH",
            "description": "Flap Diverter Valve Radiator Bypass",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "eb",
            "type": "RANGE",
            "description": "Environment Exchange Out",
            "value": "0",
            "options": null,
            "min": 0,
            "max": 100,
            "step": 5,
            "unit": "percent"
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "ec",
            "type": "RANGE",
            "description": "Environment Exchange In",
            "value": "0",
            "options": null,
            "min": 0,
            "max": 100,
            "step": 5,
            "unit": "percent"
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "f0",
            "type": "SWITCH",
            "description": "Air Hammer BSFReproduction",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "e9",
            "type": "SWITCH",
            "description": "Water Pump Relay BSFReproduction",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "f6",
            "type": "SWITCH",
            "description": "Water Pump Relay Shredder Storage",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "f8",
            "type": "SWITCH",
            "description": "Water Pump Relay Bioreactor1",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "fa",
            "type": "SWITCH",
            "description": "Water Pump Relay Bioreactor2",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "f1",
            "type": "SWITCH",
            "description": "Regen Blower",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "f2",
            "type": "SWITCH",
            "description": "BSFReproduction Light",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "f3",
            "type": "SWITCH",
            "description": "Ozone Generator",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "f4",
            "type": "SWITCH",
            "description": "UVC Light",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        }
    ],
    "sensors": {
        "py/object": "application.controller.dto.machine_sensors.Sensors",
        "shared_air": {
            "py/object": "application.controller.dto.sensors.shared_air_sensors.SharedAirSensors",
            "flowrate": null,
            "o3": null
        },
        "shredder": {
            "py/object": "application.controller.dto.sensors.shredder_sensors.ShredderSensors",
            "temperature": null,
            "humidity": null,
            "co2": null,
            "pressure": null,
            "h2": null
        },
        "bioreactor_1": {
            "py/object": "application.controller.dto.sensors.bioreactor_1_sensors.Bioreactor1Sensors",
            "temperature": null,
            "humidity": null,
            "co2": null,
            "pressure": null,
            "h2": null
        },
        "bioreactor_2": {
            "py/object": "application.controller.dto.sensors.bioreactor_2_sensors.Bioreactor2Sensors",
            "temperature": null,
            "humidity": null,
            "co2": null,
            "pressure": null,
            "h2": null
        },
        "bsf_reproduction": {
            "py/object": "application.controller.dto.sensors.bsf_reproduction_sensors.BSFReproductionSensors",
            "temperature": null,
            "humidity": null,
            "co2": null,
            "pressure": null,
            "h2": null
        }
    }
}'
{"result": "success!"}
```
