import threading
from flask import Flask

from application.controller.state import construct_state_bp
from application.mcu.actuator.air_hammer_valve_actuator import AirHammerValveActuator
from application.mcu.actuator.air_mover_actuator import AirMoverActuator
from application.mcu.actuator.bsf_light_actuator import BSFLightActuator
from application.mcu.actuator.butterfly_valve_actuator import ButterflyValveActuator
from application.mcu.actuator.discrete_flap_diverter_valve_actuator import DiscreteFlapDiverterValveActuator
from application.mcu.actuator.flap_diverter_valve_actuator import FlapDiverterValveActuator
from application.mcu.actuator.heater_relay_actuator import HeaterRelayActuator
from application.mcu.actuator.ozone_generator_actuator import OzoneGeneratorActuator
from application.mcu.actuator.rotary_diverter_valve_1_to_6_actuator import RotaryDiverterValve1To6Actuator
from application.mcu.actuator.rotary_diverter_valve_6_to_1_actuator import RotaryDiverterValve6To1Actuator
from application.mcu.actuator.water_pump_relay_actuator import WaterPumpRelayActuator
from application.mcu.measurement.co2_measurement import CO2Measurement
from application.mcu.measurement.flowrate_measurement import FlowRateMeasurement
from application.mcu.measurement.h2_measurement import H2Measurement
from application.mcu.measurement.humidity_measurement import HumidityMeasurement
from application.mcu.measurement.o3_measurement import O3Measurement
from application.mcu.measurement.pressure_measurement import PressureMeasurement
from application.mcu.measurement.state_measurement import StateMeasurement
from application.mcu.measurement.temperature_measurement import TemperatureMeasurement
from application.mcu.sensor.ds18b20_sensor import DS18B20Sensor
from application.mcu.sensor.ipc10100_sensor import IPC10100Sensor
from application.mcu.sensor.scd41_sensor import SCD41Sensor
from application.mcu.sensor.sen0321_sensor import SEN0321Sensor
from application.mcu.sensor.sen0441_sensor import SEN0441Sensor
from application.mcu.sensor.sht40_sensor import SHT40Sensor
from application.mcu.sensor.yfs201_sensor import YFS201Sensor
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

        # Temporarily modify DEVICE_MAP using DEVICE_MAP_TEMP_MAPPING (for integration testing)
        device_map_temp_mapping = app.config['DEVICE_MAP_TEMP_MAPPING']
        device_map_config = app.config['DEVICE_MAP']
        # print(f"device_map_config BEFORE:\n{device_map_config}")
        for old_id, new_id in device_map_temp_mapping.items():
            for location in device_map_config:
                if new_id in device_map_config[location]:
                    del device_map_config[location][new_id]
                if old_id in device_map_config[location]:
                    device_map_config[location][new_id] = device_map_config[location][old_id]
                    del device_map_config[location][old_id]
        # print(f"device_map_config AFTER:\n{device_map_config}")

        mcu_service = MCUService(device_types_list, measurements_list, testing=app.config['TESTING'],
                                 device_map_config=device_map_config)
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
