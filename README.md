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
Documentation: https://app.nuclino.com/Canacompost-Systems/Canacompost/API-Definition-d9f063ac-528d-462d-b2c6-4aa6d396c0e0

Examples: 
```
curl -X GET http://127.0.0.1:5000/state -H 'Content-Type: application/json' | python -m json.tool
```
```
curl -X POST http://127.0.0.1:5000/state -H 'Content-Type: application/json' -d '{"py/object":"application.controller.dto.machine_state.MachineState","actuators":[{"py/object":"application.controller.dto.actuators.actuator.Actuator","id":"e0","type":"RADIO","description":"RotaryValve1","value":"1","options":[{"py/object":"application.controller.dto.actuators.options.Options","name":"1","value":1},{"py/object":"application.controller.dto.actuators.options.Options","name":"2","value":2},{"py/object":"application.controller.dto.actuators.options.Options","name":"3","value":3},{"py/object":"application.controller.dto.actuators.options.Options","name":"4","value":4},{"py/object":"application.controller.dto.actuators.options.Options","name":"5","value":5},{"py/object":"application.controller.dto.actuators.options.Options","name":"6","value":6}],"min":null,"max":null,"step":null,"unit":null},{"py/object":"application.controller.dto.actuators.actuator.Actuator","id":"e1","type":"RADIO","description":"RotaryValve2","value":"2","options":[{"py/object":"application.controller.dto.actuators.options.Options","name":"1","value":1},{"py/object":"application.controller.dto.actuators.options.Options","name":"2","value":2},{"py/object":"application.controller.dto.actuators.options.Options","name":"3","value":3},{"py/object":"application.controller.dto.actuators.options.Options","name":"4","value":4},{"py/object":"application.controller.dto.actuators.options.Options","name":"5","value":5},{"py/object":"application.controller.dto.actuators.options.Options","name":"6","value":6}],"min":null,"max":null,"step":null,"unit":null},{"py/object":"application.controller.dto.actuators.actuator.Actuator","id":"e2","type":"RADIO","description":"RotaryValve3","value":"3","options":[{"py/object":"application.controller.dto.actuators.options.Options","name":"1","value":1},{"py/object":"application.controller.dto.actuators.options.Options","name":"2","value":2},{"py/object":"application.controller.dto.actuators.options.Options","name":"3","value":3},{"py/object":"application.controller.dto.actuators.options.Options","name":"4","value":4},{"py/object":"application.controller.dto.actuators.options.Options","name":"5","value":5},{"py/object":"application.controller.dto.actuators.options.Options","name":"6","value":6}],"min":null,"max":null,"step":null,"unit":null},{"py/object":"application.controller.dto.actuators.actuator.Actuator","id":"eb","type":"RANGE","description":"DiscreteValve1","value":"10","options":null,"min":0,"max":100,"step":10,"unit":"Percent"},{"py/object":"application.controller.dto.actuators.actuator.Actuator","id":"ec","type":"RANGE","description":"DiscreteValve2","value":"20","options":null,"min":0,"max":100,"step":10,"unit":"Percent"},{"py/object":"application.controller.dto.actuators.actuator.Actuator","id":"f4","type":"RANGE","description":"DiscreteValve3","value":"30","options":null,"min":0,"max":100,"step":10,"unit":"Percent"},{"py/object":"application.controller.dto.actuators.actuator.Actuator","id":"e7","type":"SWITCH","description":"FlapDiverterValve1","value":"false","options":null,"min":null,"max":null,"step":null,"unit":null},{"py/object":"application.controller.dto.actuators.actuator.Actuator","id":"e8","type":"SWITCH","description":"FlapDiverterValve2","value":"true","options":null,"min":null,"max":null,"step":null,"unit":null},{"py/object":"application.controller.dto.actuators.actuator.Actuator","id":"ea","type":"SWITCH","description":"FlapDiverterValve3","value":"true","options":null,"min":null,"max":null,"step":null,"unit":null},{"py/object":"application.controller.dto.actuators.actuator.Actuator","id":"f1","type":"SWITCH","description":"RegenBlower","value":"true","options":null,"min":null,"max":null,"step":null,"unit":null},{"py/object":"application.controller.dto.actuators.actuator.Actuator","id":"f3","type":"SWITCH","description":"O3Generator","value":"true","options":null,"min":null,"max":null,"step":null,"unit":null},{"py/object":"application.controller.dto.actuators.actuator.Actuator","id":"f4","type":"RANGE","description":"BlowerStrength","value":"30","options":null,"min":0,"max":100,"step":10,"unit":"Percent"},{"py/object":"application.controller.dto.actuators.actuator.Actuator","id":"ed","type":"SWITCH","description":"ShredderInValve","value":"true","options":null,"min":null,"max":null,"step":null,"unit":null},{"py/object":"application.controller.dto.actuators.actuator.Actuator","id":"e3","type":"RANGE","description":"ShredderOutValve","value":"90","options":null,"min":0,"max":100,"step":10,"unit":"Percent"},{"py/object":"application.controller.dto.actuators.actuator.Actuator","id":"f3","type":"SWITCH","description":"Bioreactor1InValve","value":"true","options":null,"min":null,"max":null,"step":null,"unit":null},{"py/object":"application.controller.dto.actuators.actuator.Actuator","id":"e4","type":"RANGE","description":"Bioreactor1OutValve","value":"90","options":null,"min":0,"max":100,"step":10,"unit":"Percent"},{"py/object":"application.controller.dto.actuators.actuator.Actuator","id":"f3","type":"SWITCH","description":"Bioreactor2InValve","value":"true","options":null,"min":null,"max":null,"step":null,"unit":null},{"py/object":"application.controller.dto.actuators.actuator.Actuator","id":"e5","type":"RANGE","description":"Bioreactor2OutValve","value":"90","options":null,"min":0,"max":100,"step":10,"unit":"Percent"},{"py/object":"application.controller.dto.actuators.actuator.Actuator","id":"f3","type":"SWITCH","description":"BSFReproductionInValve","value":"true","options":null,"min":null,"max":null,"step":null,"unit":null},{"py/object":"application.controller.dto.actuators.actuator.Actuator","id":"e6","type":"RANGE","description":"BSFReproductionOutValve","value":"90","options":null,"min":0,"max":100,"step":10,"unit":"Percent"},{"py/object":"application.controller.dto.actuators.actuator.Actuator","id":"f3","type":"SWITCH","description":"BSFReproductionLight","value":"true","options":null,"min":null,"max":null,"step":null,"unit":null}],"sensors":{"py/object":"application.controller.dto.machine_sensors.Sensors","shared_air":{"py/object":"application.controller.dto.sensors.shared_air_sensors.SharedAirSensors","pressure":50},"shredder":{"py/object":"application.controller.dto.sensors.shredder_sensors.ShredderSensors","humidity":30,"c02":5,"air_temperature":18,"soil_temperature":20},"bioreactor_1":{"py/object":"application.controller.dto.sensors.bioreactor_1_sensors.Bioreactor1Sensors","humidity":9001,"c02":5,"air_temperature":18,"soil_temperature":20},"bioreactor_2":{"py/object":"application.controller.dto.sensors.bioreactor_2_sensors.Bioreactor2Sensors","humidity":30,"c02":5,"air_temperature":18,"soil_temperature":20},"bsf_reproduction":{"py/object":"application.controller.dto.sensors.bsf_reproduction_sensors.BSFReproductionSensors","humidity":30,"c02":5,"air_temperature":18,"soil_temperature":20}}}'


curl -X POST http://127.0.0.1:5000/state -H 'Content-Type: application/json' -d '{
    "py/object": "application.controller.dto.machine_state.MachineState",
    "actuators": [
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "e0",
            "type": "RADIO",
            "description": "RotaryDiverterValveFromAirLoop",
            "value": "0",
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
            "description": "RotaryDiverterValveToAirLoop",
            "value": "0",
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
            "description": "RotaryDiverterValveCompostLoop",
            "value": "0",
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
            "description": "ButterflyValveFromShredderStorage",
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
            "description": "ButterflyValveFromBioreactor1",
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
            "description": "ButterflyValveFromBioreactor2",
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
            "description": "ButterflyValveFromBSFReproduction",
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
            "description": "FlapDiverterValveSensorLoopBypass",
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
            "description": "FlapDiverterValveRadiatorBypass",
            "value": "false",
            "options": null,
            "min": null,
            "max": null,
            "step": null,
            "unit": null
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "ea",
            "type": "SWITCH",
            "description": "FlapDiverterValveSensorBoxBypass",
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
            "description": "EnvironmentExchangeOut",
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
            "description": "EnvironmentExchangeIn",
            "value": "20",
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
            "description": "AirHammerBSFReproduction",
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
            "type": "RANGE",
            "description": "RegenBlowerOutputStrengthModerator",
            "value": "0",
            "options": null,
            "min": 0,
            "max": 100,
            "step": 5,
            "unit": "percent"
        },
        {
            "py/object": "application.controller.dto.actuators.actuator.Actuator",
            "id": "f1",
            "type": "SWITCH",
            "description": "RegenBlower",
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