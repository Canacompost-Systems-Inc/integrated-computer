# Integrated Computer

## Getting Started 
1. Install Python3 - https://www.python.org/downloads/
2. Download pip (Google instructions per OS)
3. `python3 -m venv venv` to create a virtual environment. This is used to manage Python dependencies within just the context of your terminal instance. 
4. `source venv/bin/activate` to start your virtual environment 
5. `pip install -r requirements.txt` to install all project dependencies 
6. `FLASK_ENV=development flask run --no-reload` to run the server in your terminal. The server will live update as you make code changes. 
7. If the above command does not work, try: `python3 wsgi.py`

### Resources and Documentation
1. API Docs:
   1. [Measurement Schema](./docs/schema/measurement.md)
   2. [Meta State Schema](./docs/schema/meta_state.md)
   3. [Routine Schema](./docs/schema/routine.md)
   4. [State Schema](./docs/schema/state.md)
   5. [Task Queue Schema](./docs/schema/task_queue.md)
2. [Sensor and Actuator Source of Truth](./docs/sensor_actuator_source_truth.md)
3. [Original API Definition](https://app.nuclino.com/Canacompost-Systems/Canacompost/API-Definition-d9f063ac-528d-462d-b2c6-4aa6d396c0e0)
4. [Flask Documentation](https://flask.palletsprojects.com/en/2.0.x/)

## Note on the Project Structure 
The project has been designed to follow the pattern of [dependency injection](https://en.wikipedia.org/wiki/Dependency_injection). Each layer has its dependencies injected in the `app.py` file to limit coupling between components. 

## Testing
Using the APIs below, routines can be manually test run, and sensor values can be manually set to test the state machine.
