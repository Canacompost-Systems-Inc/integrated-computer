import threading
from flask import Flask
from flask_cors import CORS

from application.controller.measurement import construct_measurement_bp
from application.controller.meta_state import construct_meta_state_bp
from application.controller.routine import construct_routine_bp
from application.controller.state import construct_state_bp
from application.controller.task_queue import construct_task_queue_bp
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
from application.model.actuator.uvc_light import UVCLightActuator
from application.model.actuator.water_pump_relay_actuator import WaterPumpRelayActuator
from application.model.context.isolation_context import IsolationContext
from application.model.location.airloop_location import AirLoopLocation
from application.model.location.bioreactor1_location import Bioreactor1Location
from application.model.location.bioreactor2_location import Bioreactor2Location
from application.model.location.bsfreproduction_location import BSFReproductionLocation
from application.model.location.compostloop_location import CompostLoopLocation
from application.model.location.shredderstorage_location import ShredderStorageLocation
from application.model.location.sieve_location import SieveLocation
from application.model.measurement.co2_measurement import CO2Measurement
from application.model.measurement.flowrate_measurement import FlowRateMeasurement
from application.model.measurement.h2_measurement import H2Measurement
from application.model.measurement.humidity_measurement import HumidityMeasurement
from application.model.measurement.o3_measurement import O3Measurement
from application.model.measurement.pressure_measurement import PressureMeasurement
from application.model.measurement.state_measurement import StateMeasurement
from application.model.measurement.temperature_measurement import TemperatureMeasurement
from application.model.routine.cool_and_dehumidify_bioreactor_1_routine import CoolAndDehumidifyBioreactor1Routine
from application.model.routine.cool_and_dehumidify_bioreactor_2_routine import CoolAndDehumidifyBioreactor2Routine
from application.model.routine.cool_and_dehumidify_bsf_reproduction_routine import \
    CoolAndDehumidifyBSFReproductionRoutine
from application.model.routine.cool_and_dehumidify_shredder_storage_routine import \
    CoolAndDehumidifyShredderStorageRoutine
from application.model.routine.flush_air_loop_routine import FlushAirLoopRoutine
from application.model.routine.flush_compost_loop_routine import FlushCompostLoopRoutine
from application.model.routine.heat_bioreactor_1_routine import HeatBioreactor1Routine
from application.model.routine.heat_bioreactor_2_routine import HeatBioreactor2Routine
from application.model.routine.heat_bsf_reproduction_routine import HeatBSFReproductionRoutine
from application.model.routine.heat_shredder_storage_routine import HeatShredderStorageRoutine
from application.model.routine.humidify_bioreactor_1_routine import HumidifyBioreactor1Routine
from application.model.routine.humidify_bioreactor_2_routine import HumidifyBioreactor2Routine
from application.model.routine.humidify_bsf_reproduction_routine import HumidifyBSFReproductionRoutine
from application.model.routine.humidify_shredder_storage_routine import HumidifyShredderStorageRoutine
from application.model.routine.move_compost.move_compost_from_bioreactor_1_to_bsf_reproduction_routine import \
    MoveCompostFromBioreactor1ToBSFReproductionRoutine
from application.model.routine.move_compost.move_compost_from_bioreactor_1_to_shredder_storage_routine import \
    MoveCompostFromBioreactor1ToShredderStorageRoutine
from application.model.routine.move_compost.move_compost_from_bioreactor_2_to_bsf_reproduction_routine import \
    MoveCompostFromBioreactor2ToBSFReproductionRoutine
from application.model.routine.move_compost.move_compost_from_bioreactor_2_to_shredder_storage_routine import \
    MoveCompostFromBioreactor2ToShredderStorageRoutine
from application.model.routine.move_compost.move_compost_from_bsf_reproduction_to_bioreactor_1_routine import \
    MoveCompostFromBSFReproductionToBioreactor1Routine
from application.model.routine.move_compost.move_compost_from_bsf_reproduction_to_bioreactor_2_routine import \
    MoveCompostFromBSFReproductionToBioreactor2Routine
from application.model.routine.move_compost.move_compost_from_bsf_reproduction_to_sieve_routine import \
    MoveCompostFromBSFReproductionToSieveRoutine
from application.model.routine.move_compost.move_compost_from_shredder_storage_to_bioreactor_1_routine import \
    MoveCompostFromShredderStorageToBioreactor1Routine
from application.model.routine.move_compost.move_compost_from_shredder_storage_to_bioreactor_2_routine import \
    MoveCompostFromShredderStorageToBioreactor2Routine
from application.model.routine.read_sensors_bioreactor_1_routine import ReadSensorsBioreactor1Routine
from application.model.routine.read_sensors_bioreactor_2_routine import ReadSensorsBioreactor2Routine
from application.model.routine.read_sensors_bsf_reproduction_routine import ReadSensorsBSFReproductionRoutine
from application.model.routine.read_sensors_realtime_routine import ReadSensorsRealtimeRoutine
from application.model.routine.read_sensors_shredder_storage_routine import ReadSensorsShredderStorageRoutine
from application.model.routine.sanitize_air_loop_routine import SanitizeAirLoopRoutine
from application.model.routine.sanitize_compost_loop_routine import SanitizeCompostLoopRoutine
from application.model.sensor.ds18b20_sensor import DS18B20Sensor
from application.model.sensor.ipc10100_sensor import IPC10100Sensor
from application.model.sensor.scd41_sensor import SCD41Sensor
from application.model.sensor.sen0321_sensor import SEN0321Sensor
from application.model.sensor.sen0441_sensor import SEN0441Sensor
from application.model.sensor.sht40_sensor import SHT40Sensor
from application.model.sensor.yfs201_sensor import YFS201Sensor
from application.model.state.isolation.air_loop_bioreactor_1_state import AirLoopBioreactor1State
from application.model.state.isolation.air_loop_bioreactor_2_state import AirLoopBioreactor2State
from application.model.state.isolation.air_loop_bsf_reproduction_state import AirLoopBSFReproductionState
from application.model.state.isolation.air_loop_shredder_storage_state import AirLoopShredderStorageState
from application.model.state.isolation.compost_loop_bioreactor_1_state import CompostLoopBioreactor1State
from application.model.state.isolation.compost_loop_bioreactor_2_state import CompostLoopBioreactor2State
from application.model.state.isolation.compost_loop_bsf_reproduction_state import CompostLoopBSFReproductionState
from application.model.state.isolation.compost_loop_shredder_storage_state import CompostLoopShredderStorageState
from application.model.state.isolation.default_state import DefaultState
from application.service.device_factory import DeviceFactory
from application.service.device_registry_service import DeviceRegistryService
from application.service.dto_translator_service import DtoTranslatorService
from application.service.isolation_state_registry_service import IsolationStateRegistryService
from application.service.location_registry_service import LocationRegistryService
from application.service.mcu_service import MCUService
from application.service.measurement_factory import MeasurementFactory
from application.service.state_manager import StateManager
from application.service.routine_registry_service import RoutineRegistryService
from application.persistence.mcu_persistent import MCUPersistent
from application.service.mcu_state_tracker_service import MCUStateTrackerService

# Globally accessible connections / plugins / etc.
mcu = MCUPersistent()


def init_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('application.config.Config')

    CORS(app)

    # Initialize connections / plugins / etc.
    mcu.init_app(app)

    with app.app_context():

        location_list = [
            AirLoopLocation,
            Bioreactor1Location,
            Bioreactor2Location,
            BSFReproductionLocation,
            CompostLoopLocation,
            ShredderStorageLocation,
            SieveLocation,
        ]
        location_registry_service = LocationRegistryService(location_list)

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
            UVCLightActuator,
            WaterPumpRelayActuator,
        ]
        device_factory = DeviceFactory(device_types_list)
        device_registry_service = DeviceRegistryService(device_factory, location_registry_service,
                                                        app.config['DEVICE_MAP'],
                                                        app.config['LOCATION_AWARE_SENSORS'])

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
        measurement_factory = MeasurementFactory(measurements_list)

        mcu_service = MCUService(device_registry_service, measurement_factory, testing=app.config['TESTING'],
                                 demo_mode=app.config['DEMO_MODE'])

        isolation_state_list = [
            AirLoopBioreactor1State,
            AirLoopBioreactor2State,
            AirLoopBSFReproductionState,
            AirLoopShredderStorageState,
            CompostLoopBioreactor1State,
            CompostLoopBioreactor2State,
            CompostLoopBSFReproductionState,
            CompostLoopShredderStorageState,
            DefaultState,
        ]
        isolation_context = IsolationContext()
        isolation_state_registry_service = IsolationStateRegistryService(isolation_state_list, isolation_context)

        routine_list = [
            CoolAndDehumidifyBioreactor1Routine,
            CoolAndDehumidifyBioreactor2Routine,
            CoolAndDehumidifyBSFReproductionRoutine,
            CoolAndDehumidifyShredderStorageRoutine,
            FlushAirLoopRoutine,
            FlushCompostLoopRoutine,
            HeatBioreactor1Routine,
            HeatBioreactor2Routine,
            HeatBSFReproductionRoutine,
            HeatShredderStorageRoutine,
            HumidifyBioreactor1Routine,
            HumidifyBioreactor2Routine,
            HumidifyBSFReproductionRoutine,
            HumidifyShredderStorageRoutine,
            MoveCompostFromBioreactor1ToBSFReproductionRoutine,
            MoveCompostFromBioreactor1ToShredderStorageRoutine,
            MoveCompostFromBioreactor2ToBSFReproductionRoutine,
            MoveCompostFromBioreactor2ToShredderStorageRoutine,
            MoveCompostFromBSFReproductionToBioreactor1Routine,
            MoveCompostFromBSFReproductionToBioreactor2Routine,
            MoveCompostFromBSFReproductionToSieveRoutine,
            MoveCompostFromShredderStorageToBioreactor1Routine,
            MoveCompostFromShredderStorageToBioreactor2Routine,
            ReadSensorsBioreactor1Routine,
            ReadSensorsBioreactor2Routine,
            ReadSensorsBSFReproductionRoutine,
            ReadSensorsRealtimeRoutine,
            ReadSensorsShredderStorageRoutine,
            SanitizeAirLoopRoutine,
            SanitizeCompostLoopRoutine,
        ]
        routine_list = [r for r in routine_list if r.name not in app.config['DISABLED_ROUTINES']]
        routines_registry_service = RoutineRegistryService(routine_list)

        mcu_state_tracker_service = MCUStateTrackerService(device_registry_service, location_registry_service,
                                                           isolation_context)
        state_manager = StateManager(mcu_state_tracker_service, mcu_service, isolation_state_registry_service,
                                     isolation_context,
                                     disable_routines_between=app.config['DISABLE_ROUTINES_BETWEEN'])

        # Construct blueprints
        dto_translator_service = DtoTranslatorService(device_registry_service)
        state_controller = construct_state_bp(state_manager, mcu_state_tracker_service, dto_translator_service)
        meta_state_controller = construct_meta_state_bp(state_manager)
        routine_controller = construct_routine_bp(routines_registry_service)
        task_queue_controller = construct_task_queue_bp(state_manager, routines_registry_service,
                                                        isolation_state_registry_service)
        measurement_controller = construct_measurement_bp(measurement_factory)

        # Register API controller blueprints
        app.register_blueprint(state_controller)
        app.register_blueprint(meta_state_controller)
        app.register_blueprint(routine_controller)
        app.register_blueprint(task_queue_controller)
        app.register_blueprint(measurement_controller)

        # Define a wrapper function to restart the thread if it dies
        def restart_thread_wrapper(thread_func):
            def wrapper():
                while True:
                    try:
                        thread_func()
                    except BaseException as e:
                        import traceback
                        traceback.print_exc()
                        app.logger.error(f"{e}; restarting thread")
                    else:
                        app.logger.error(f"Thread exited normally, which shouldn't happen; restarting thread")

            return wrapper

        # Start the MCU manager thread. Other threads may also be required, such as polling loops to the MCUs.
        # Implementation is pending the design on how MCUs and the service will communicate
        thread = threading.Thread(target=restart_thread_wrapper(state_manager.manage_state))
        thread.start()

    return app
