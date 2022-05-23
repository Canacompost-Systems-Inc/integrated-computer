# Getting Started 
1. Install Python3 - https://www.python.org/downloads/
2. Download pip (Google instructions per OS)
3. `python3 -m venv venv` to create a virtual environment. This is used to manage Python dependencies within just the context of your terminal instance. 
4. `source venv/bin/activate` to start your virtual environment 
5. `pip install -r requirements.txt` to install all project dependencies 
6. `FLASK_ENV=development flask run` to run the server in your terminal. The server will live update as you make code changes. 

# Helpful docs 
1. [Flask Documentation](https://flask.palletsprojects.com/en/2.0.x/)

# Testing
Using the APIs below, routines can be manually test run, and sensor values can be manually set to test the state machine.

# Note on the Project Structure 
The project has been designed to follow the pattern of [dependency injection](https://en.wikipedia.org/wiki/Dependency_injection). Each layer has its dependencies injected in the `app.py` file to limit coupling between components. 

# API
`/oxygen` - Supports `GET` and `POST`. Get and set the oxygen sensor value. Examples: 
```
curl -X GET http://127.0.0.1:5000/oxygen -H 'Content-Type: application/json' 
curl -X POST http://127.0.0.1:5000/oxygen -H 'Content-Type: application/json' -d  '{"value": "15"}'
```

`/temperature` - Supports `GET` and `POST`. Get and set the temperature sensor value. Examples: 
```
curl -X GET http://127.0.0.1:5000/temperature -H 'Content-Type: application/json' 
curl -X POST http://127.0.0.1:5000/temperature -H 'Content-Type: application/json' -d  '{"value": "35"}'
```

`/humidity` - Supports `GET` and `POST`. Get and set the humidity sensor value. Examples: 
```
curl -X GET http://127.0.0.1:5000/humidity -H 'Content-Type: application/json' 
curl -X POST http://127.0.0.1:5000/humidity -H 'Content-Type: application/json' -d  '{"value": "75"}'
```

`/bsfl` - Supports `GET` and `POST`. Get and set the state of BSFL. Examples: 
```
curl -X GET http://127.0.0.1:5000/bsfl -H 'Content-Type: application/json' 
curl -X POST http://127.0.0.1:5000/bsfl -H 'Content-Type: application/json' -d  '{"value": "True"}'
```

`/r0` - Supports `GET` and `POST`. Start routine 0. Examples: 
```
curl -X GET http://127.0.0.1:5000/r0 
curl -X POST http://127.0.0.1:5000/r0 
```

`/r1` - Supports `GET` and `POST`. Start routine 1.   
`/r2` - Supports `GET` and `POST`. Start routine 2.   
`/r3` - Supports `GET` and `POST`. Start routine 3.   
`/r4` - Supports `GET` and `POST`. Start routine 4.    
`/r5` - Supports `GET` and `POST`. Start routine 5.   