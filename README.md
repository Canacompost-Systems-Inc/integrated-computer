# Getting Started 
1. Install Python3 - https://www.python.org/downloads/
2. Download pip (Google instructions per OS)
3. `python3 -m venv venv` to create a virtual environment. This is used to manage Python dependencies within just the context of your terminal instance. 
4. `source venv/bin/activate` to start your virtual environment 
5. `pip install -r requirements.txt` to install all project dependencies 
6. `FLASK_ENV=development flask run --no-reload` to run the server in your terminal. The server will live update as you make code changes. 
7. If the above command does not work, try: `python3 wsgi.py`

# Helpful docs 
1. [Flask Documentation](https://flask.palletsprojects.com/en/2.0.x/)

# Note on the Project Structure 
The project has been designed to follow the pattern of [dependency injection](https://en.wikipedia.org/wiki/Dependency_injection). Each layer has its dependencies injected in the `app.py` file to limit coupling between components. 

# Testing
Using the APIs below, routines can be manually test run, and sensor values can be manually set to test the state machine.

# API

## Meta-state
Examples: 
```
curl -X GET http://127.0.0.1:5000/meta_state -H 'Content-Type: application/json' | python -m json.tool

curl -X POST http://127.0.0.1:5000/meta_state -H 'Content-Type: application/json' -d '{
    "py/object": "application.controller.dto.system_meta_state.SystemMetaState",
    "disable_automated_routines": true
}'
```

## State
Documentation: https://app.nuclino.com/Canacompost-Systems/Canacompost/API-Definition-d9f063ac-528d-462d-b2c6-4aa6d396c0e0

Examples: 
```
curl -X GET http://127.0.0.1:5000/state -H 'Content-Type: application/json' | python -m json.tool
```
```
curl -X POST http://127.0.0.1:5000/state -H 'Content-Type: application/json' -d '{
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
```