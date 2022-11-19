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
curl -X GET http://127.0.0.1:5000/state -H 'Content-Type: application/json' 
```
```
curl -X POST http://127.0.0.1:5000/state -H 'Content-Type: application/json' -d  '
{
    "actuators":[
        {
            "id": "e0",
            "type": "RADIO",
            "description": "Rotary Valve 1",
            "value": "1",
            "options": [
                {
                    "name": "1",
                    "value": 1
                },
                {
                    "name": "2",
                    "value": 2
                },
                {
                    "name": "3",
                    "value": 3v
                },
                {
                    "name": "4",
                    "value": 4
                },
                {
                    "name": "5",
                    "value": 5
                },
                {
                    "name": "6",
                    "value": 6
                }
            ]
        },
        {
            "id": "e1",
            "type": "RADIO",
            "description": "Rotary Valve 2",
            "value": "2",
            "options": [
                {
                    "name": "1",
                    "value": 1
                },
                {
                    "name": "2",
                    "value": 2
                },
                {
                    "name": "3",
                    "value": 3
                },
                {
                    "name": "4",
                    "value": 4
                },
                {
                    "name": "5",
                    "value": 5
                },
                {
                    "name": "6",
                    "value": 6
                }
            ]
        },
        {
            "id": "e2",
            "type": "RADIO",
            "description": "Rotary Valve 3",
            "value": "3",
            "options": [
                {
                    "name": "1",
                    "value": 1
                },
                {
                    "name": "2",
                    "value": 2
                },
                {
                    "name": "3",
                    "value": 3
                },
                {
                    "name": "4",
                    "value": 4
                },
                {
                    "name": "5",
                    "value": 5
                },
                {
                    "name": "6",
                    "value": 6
                }
            ]
        },
        {
            "id": "eb",
            "type": "RANGE",
            "description": "Discrete Valve 1",
            "value": "10",
            "min": 0,
            "max": 100,
            "step": 10,
            "unit": "Percent"
        },
        {
            "id": "ec",
            "type": "RANGE",
            "description": "Discrete Valve 2",
            "value": "20",
            "min": 0,
            "max": 100,
            "step": 10,
            "unit": "Percent"
        },
        {
            "id": "f4",
            "type": "RANGE",
            "description": "Discrete Valve 3",
            "value": "30",
            "min": 0,
            "max": 100,
            "step": 10,
            "unit": "Percent"
        },
        {
            "id": "e7",
            "type": "SWITCH",
            "description": "Flap Diverter Valve 1",
            "value": "false"
        },
        {
            "id": "e8",
            "type": "SWITCH",
            "description": "Flap Diverter Valve 2",
            "value": "true"
        },
        {
            "id": "ea",
            "type": "SWITCH",
            "description": "Flap Diverter Valve 3",
            "value": "true"
        },
        {
            "id": "f1",
            "type": "SWITCH",
            "description": "Regen Blower",
            "value": "true"
        },
        {
            "id": "f3",
            "type": "SWITCH",
            "description": "O3 Generator",
            "value": "true"
        },
        {
            "id": "f4",
            "type": "RANGE",
            "description": "Blower Strength",
            "value": "30",
            "min": 0,
            "max": 100,
            "step": 10,
            "unit": "Percent"
        },
        {
            "id": "ed",
            "type": "SWITCH",
            "description": "Shredder In Valve",
            "value": "true"
        },
        {
            "id": "e3",
            "type": "RANGE",
            "description": "Shredder Out Valve",
            "value": "90",
            "min": 0,
            "max": 100,
            "step": 10,
            "unit": "Percent"
        },
        {
            "id": "f3",
            "type": "SWITCH",
            "description": "Bioreactor 1 In Valve",
            "value": "true"
        },
        {
            "id": "e4",
            "type": "RANGE",
            "description": "Bioreactor 1 Out Valve",
            "value": "90",
            "min": 0,
            "max": 100,
            "step": 10,
            "unit": "Percent"
        },
        {
            "id": "f3",
            "type": "SWITCH",
            "description": "Bioreactor 2 In Valve",
            "value": "true"
        },
        {
            "id": "e5",
            "type": "RANGE",
            "description": "Bioreactor 2 Out Valve",
            "value": "90",
            "min": 0,
            "max": 100,
            "step": 10,
            "unit": "Percent"
        },
        {
            "id": "f3",
            "type": "SWITCH",
            "description": "BSF Reproduction In Valve",
            "value": "true"
        },
        {
            "id": "e6",
            "type": "RANGE",
            "description": "BSF Reproduction Out Valve",
            "value": "90",
            "min": 0,
            "max": 100,
            "step": 10,
            "unit": "Percent"
        },
        {
            "id": "f3",
            "type": "SWITCH",
            "description": "BSF Reproduction Light",
            "value": "true"
        }
    ],
    "sensors":{
       "shared_air":{
            "pressure":50
       },
       "shredder":{
            "humidity":30,
            "c02":5,
            "air_temperature":18,
            "soil_temperature":20
       },
       "bioreactor_1":{
            "humidity":30,
            "c02":5,
            "air_temperature":18,
            "soil_temperature":20
       },
       "bioreactor_2":{
            "humidity":30,
            "c02":5,
            "air_temperature":18,
            "soil_temperature":20
       },
       "bsf_reproduction":{
            "humidity":30,
            "c02":5,
            "air_temperature":18,
            "soil_temperature":20
       }
    }
 }
'
```