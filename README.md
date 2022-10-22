# Getting Started 
1. Install Python3 - https://www.python.org/downloads/
2. Download pip (Google instructions per OS)
3. `python3 -m venv venv` to create a virtual environment. This is used to manage Python dependencies within just the context of your terminal instance. 
4. `source venv/bin/activate` to start your virtual environment 
5. `pip install -r requirements.txt` to install all project dependencies 
6. `FLASK_ENV=development flask run --no-reload` to run the server in your terminal. The server will live update as you make code changes. 

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
    "actuators":{
    "type": "object",
        "shared_air":{
            "rotary_valve_1":1,
            "rotary_valve_2":2,
            "rotary_valve_3":3,
            "discrete_valve_1":10,
            "discrete_valve_2":20,
            "discrete_valve_3":30,
            "flap_valve_1":true,
            "flap_valve_2":false,
            "flap_valve_3":true,
            "blower_on":true,
            "o3_generator":true,
            "blower_strength":50
       },
       "shredder":{
            "out_valve":true,
            "in_valve":false
       },
       "bioreactor_1":{
            "out_valve":true,
            "in_valve":false
       },
       "bioreactor_2":{
            "out_valve":true,
            "in_valve":false
       },
       "bsf_reproduction":{
            "out_valve":true,
            "in_valve":false,
            "light":true
       }
    },
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