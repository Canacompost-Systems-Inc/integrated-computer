import threading
from flask import Flask

from application.controller.bsfl import construct_bsfl_bp
from application.controller.oxygen import construct_oxygen_bp
from application.controller.temperature import construct_temperature_bp
from application.controller.humidity import construct_humidity_bp
from application.controller.routines import construct_r0_bp, construct_r1_bp, construct_r2_bp, construct_r3_bp,\
    construct_r4_bp, construct_r5_bp
from application.mcu.bsfl_effector import BSFLEffector
from application.mcu.measurement.co2_measurement import CO2Measurement
from application.mcu.measurement.humidity_measurement import HumidityMeasurement
from application.mcu.measurement.pressure_measurement import PressureMeasurement
from application.mcu.measurement.temperature_measurement import TemperatureMeasurement
from application.mcu.oxygen_effector import OxygenEffector
from application.mcu.temperature_effector import TemperatureEffector
from application.mcu.humidity_effector import HumidityEffector
from application.mcu.valve_effector import ValvesEffector
from application.mcu.compressor_effector import CompressorEffector
from application.mcu.water_pump_effector import WaterPumpEffector
from application.mcu.sensor.ds18b20_sensor import DS18B20Sensor
from application.mcu.sensor.ipc10100_sensor import IPC10100Sensor
from application.mcu.sensor.scd41_sensor import SCD41Sensor
from application.mcu.sensor.sht40_sensor import SHT40Sensor
from application.service.bsfl import BSFLService
from application.service.humidity import HumidityService
from application.service.mcu import MCUService
from application.service.mcu_manager import StateManager
from application.service.oxygen import OxygenService
from application.service.routines import RoutinesService
from application.service.temperature import TemperatureService
from application.service.valves import ValvesService
from application.service.compressor import CompressorService
from application.service.water_pump import WaterPumpService
from application.mcu_persistent import MCUPersistent

# Globally accessible connections / plugins / etc.
mcu = MCUPersistent()


def init_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('application.config.Config')

    # Initialize connections / plugins / etc.
    mcu.init_app(app)

    with app.app_context():

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
        sensor_list = [
            SHT40Sensor(),
            SCD41Sensor(),
            IPC10100Sensor(),
            DS18B20Sensor()
        ]
        measurements_list = [
            CO2Measurement,
            HumidityMeasurement,
            PressureMeasurement,
            TemperatureMeasurement
        ]
        mcu_service = MCUService(sensor_list, measurements_list, testing=app.config['TESTING'])
        state_manager = StateManager(oxygen_service, temperature_service, humidity_service, bsfl_service,
                                     compressor_service, routines_service, mcu_service)

        # Construct blueprints
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

        # Register API controller blueprints
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

        # Start the MCU manager thread. Other threads may also be required, such as polling loops to the MCUs.
        # Implementation is pending the design on how MCUs and the service will communicate
        thread = threading.Thread(target=state_manager.manage_state)
        thread.start()

    return app
