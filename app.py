import threading
from flask import Flask
from mcu.oxygen_effector import *
from mcu.temperature_effector import *
from controller.oxygen import *
from controller.temperature import *
from service.mcu_manager import *

app = Flask(__name__)

oxygen_effector = OxygenEffector()
temperature_effector = TemperatureEffector()
state_manager = StateManager(oxygen_effector, temperature_effector)
oxygen_service = OxygenService(oxygen_effector)
temperature_service = TemperatureService(temperature_effector)
oxygen_controller = construct_oxygen_bp(oxygen_service)
temperature_controller = construct_temperature_bp(temperature_service)

@app.before_first_request
def activate_job():
    # Start the MCU manager thread. Other threads may also be required, such as polling loops to the MCUs. 
    # Implementation is pending the design on how MCUs and the service will communicate
    thread = threading.Thread(target=state_manager.manage_state)
    thread.start()

# Register API controllers
app.register_blueprint(oxygen_controller)
app.register_blueprint(temperature_controller)

if __name__ == "__main__":
    app.run()