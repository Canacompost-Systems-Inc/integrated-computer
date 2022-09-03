import threading
from flask import Flask
from controller.bsfl import construct_bsfl_bp
from mcu.bsfl_effector import BSFLEffector
from mcu.oxygen_effector import *
from mcu.temperature_effector import *
from mcu.humidity_effector import *
from mcu.valve_effector import *
from mcu.compressor_effector import *
from mcu.water_pump_effector import *
from controller.oxygen import *
from controller.temperature import *
from controller.humidity import *
from controller.routines import *
from service.bsfl import BSFLService
from service.mcu_manager import *
from service.routines import *
from service.valves import *
from service.compressor import *
from service.water_pump import *
from service.mcu import *

app = Flask(__name__)

oxygen_effector = OxygenEffector()
temperature_effector = TemperatureEffector()
humidity_effector = HumidityEffector()
bsfl_effector = BSFLEffector()
valves_effector = ValvesEffector()
compressor_effector = CompressorEffector()
water_pump_effector = WaterPumpEffector()
oxygen_service = OxygenService(oxygen_effector)
humidity_service = HumidityService(humidity_effector)
temperature_service = TemperatureService(temperature_effector)
bsfl_service = BSFLService(bsfl_effector)
valves_service = ValvesService(valves_effector)
compressor_service = CompressorService(compressor_effector)
water_pump_service = WaterPumpService(water_pump_effector)
routines_service = RoutinesService(valves_service, compressor_service, water_pump_service)
mcu_service = MCUService()
state_manager = StateManager(oxygen_service, temperature_service, humidity_service, bsfl_service, compressor_service, routines_service, mcu_service)
oxygen_controller = construct_oxygen_bp(oxygen_service)
temperature_controller = construct_temperature_bp(temperature_service)
humidity_controller = construct_humidity_bp(humidity_service)
bsfl_controller = construct_bsfl_bp(bsfl_service)
r0_controller = construct_r0_bp(routines_service)
r1_controller = construct_r1_bp(routines_service)
r2_controller = construct_r2_bp(routines_service)
r3_controller = construct_r3_bp(routines_service)
r4_controller = construct_r4_bp(routines_service)
r5_controller = construct_r5_bp(routines_service)

@app.before_first_request
def activate_job():
    # Start the MCU manager thread. Other threads may also be required, such as polling loops to the MCUs. 
    # Implementation is pending the design on how MCUs and the service will communicate
    thread = threading.Thread(target=state_manager.manage_state)
    thread.start()

# Register API controllers
app.register_blueprint(oxygen_controller)
app.register_blueprint(temperature_controller)
app.register_blueprint(humidity_controller)
app.register_blueprint(bsfl_controller)
app.register_blueprint(r0_controller)
app.register_blueprint(r1_controller)
app.register_blueprint(r2_controller)
app.register_blueprint(r3_controller)
app.register_blueprint(r4_controller)
app.register_blueprint(r5_controller)

if __name__ == "__main__":
    app.run()