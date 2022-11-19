import threading
from flask import Flask

from application.controller.state import construct_state_bp
from application.mcu.actuator.air_hammer_valve_actuator import AirHammerValveActuator
from application.mcu.actuator.air_mover_actuator import AirMoverActuator
from application.mcu.actuator.bsf_light_actuator import BSFLightActuator
from application.mcu.actuator.butterfly_valve_actuator import ButterflyValveActuator
from application.mcu.actuator.discrete_flap_diverter_valve_actuator import DiscreteFlapDiverterValveActuator
from application.mcu.actuator.flap_diverter_valve_actuator import FlapDiverterValveActuator
from application.mcu.actuator.rotary_diverter_valve_1_to_6_actuator import RotaryDiverterValve1To6Actuator
from application.mcu.actuator.rotary_diverter_valve_6_to_1_actuator import RotaryDiverterValve6To1Actuator
from application.mcu.measurement.co2_measurement import CO2Measurement
from application.mcu.measurement.humidity_measurement import HumidityMeasurement
from application.mcu.measurement.pressure_measurement import PressureMeasurement
from application.mcu.measurement.state_measurement import StateMeasurement
from application.mcu.measurement.temperature_measurement import TemperatureMeasurement
from application.mcu.sensor.ds18b20_sensor import DS18B20Sensor
from application.mcu.sensor.ipc10100_sensor import IPC10100Sensor
from application.mcu.sensor.scd41_sensor import SCD41Sensor
from application.mcu.sensor.sht40_sensor import SHT40Sensor
from application.service.mcu import MCUService
from application.service.mcu_manager import StateManager
from application.service.routines import RoutinesService
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

        routines_service = RoutinesService()
        device_types_list = [
            SHT40Sensor,
            SCD41Sensor,
            IPC10100Sensor,
            DS18B20Sensor,
            AirMoverActuator,
            AirHammerValveActuator,
            BSFLightActuator,
            ButterflyValveActuator,
            DiscreteFlapDiverterValveActuator,
            FlapDiverterValveActuator,
            RotaryDiverterValve1To6Actuator,
            RotaryDiverterValve6To1Actuator,
        ]
        measurements_list = [
            CO2Measurement,
            HumidityMeasurement,
            PressureMeasurement,
            TemperatureMeasurement,
            StateMeasurement,
        ]
        mcu_service = MCUService(device_types_list, measurements_list, testing=app.config['TESTING'],
                                 device_map_config=app.config['DEVICE_MAP'])
        state_manager = StateManager(routines_service, mcu_service)

        # Construct blueprints
        # TODO - add in a construct_sensors_bp?
        state_controller = construct_state_bp()

        # Register API controller blueprints
        # TODO - register blueprint
        app.register_blueprint(state_controller)

        # Start the MCU manager thread. Other threads may also be required, such as polling loops to the MCUs.
        # Implementation is pending the design on how MCUs and the service will communicate
        thread = threading.Thread(target=state_manager.manage_state)
        thread.start()

    return app
