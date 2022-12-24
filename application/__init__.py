import threading
from flask import Flask

from application.controller.state import construct_state_bp
from application.model.actuator.air_hammer_valve_actuator import AirHammerValveActuator
from application.model.actuator.air_mover_actuator import AirMoverActuator
from application.model.actuator.bsf_light_actuator import BSFLightActuator
from application.model.actuator.butterfly_valve_actuator import ButterflyValveActuator
from application.model.actuator.discrete_flap_diverter_valve_actuator import DiscreteFlapDiverterValveActuator
from application.model.actuator.flap_diverter_valve_actuator import FlapDiverterValveActuator
from application.model.actuator.heater_relay_actuator import HeaterRelayActuator
from application.model.actuator.ozone_generator_actuator import OzoneGeneratorActuator
from application.model.actuator.rotary_diverter_valve_1_to_6_actuator import RotaryDiverterValve1To6Actuator
from application.model.actuator.rotary_diverter_valve_6_to_1_actuator import RotaryDiverterValve6To1Actuator
from application.model.actuator.water_pump_relay_actuator import WaterPumpRelayActuator
from application.model.measurement.co2_measurement import CO2Measurement
from application.model.measurement.flowrate_measurement import FlowRateMeasurement
from application.model.measurement.h2_measurement import H2Measurement
from application.model.measurement.humidity_measurement import HumidityMeasurement
from application.model.measurement.o3_measurement import O3Measurement
from application.model.measurement.pressure_measurement import PressureMeasurement
from application.model.measurement.state_measurement import StateMeasurement
from application.model.measurement.temperature_measurement import TemperatureMeasurement
from application.model.sensor.ds18b20_sensor import DS18B20Sensor
from application.model.sensor.ipc10100_sensor import IPC10100Sensor
from application.model.sensor.scd41_sensor import SCD41Sensor
from application.model.sensor.sen0321_sensor import SEN0321Sensor
from application.model.sensor.sen0441_sensor import SEN0441Sensor
from application.model.sensor.sht40_sensor import SHT40Sensor
from application.model.sensor.yfs201_sensor import YFS201Sensor
from application.service.mcu_service import MCUService
from application.service.state_manager import StateManager
from application.service.routines import RoutinesService
from application.persistence.mcu_persistent import MCUPersistent

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
            DS18B20Sensor,
            IPC10100Sensor,
            SCD41Sensor,
            SEN0321Sensor,
            SEN0441Sensor,
            SHT40Sensor,
            YFS201Sensor,
            AirMoverActuator,
            AirHammerValveActuator,
            BSFLightActuator,
            ButterflyValveActuator,
            DiscreteFlapDiverterValveActuator,
            FlapDiverterValveActuator,
            HeaterRelayActuator,
            OzoneGeneratorActuator,
            RotaryDiverterValve1To6Actuator,
            RotaryDiverterValve6To1Actuator,
            WaterPumpRelayActuator,
        ]
        measurements_list = [
            CO2Measurement,
            FlowRateMeasurement,
            H2Measurement,
            HumidityMeasurement,
            O3Measurement,
            PressureMeasurement,
            TemperatureMeasurement,
            StateMeasurement,
        ]
        mcu_service = MCUService(device_types_list, measurements_list, device_map_config=app.config['DEVICE_MAP'],
                                 testing=app.config['TESTING'])
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
