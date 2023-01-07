from flask import Blueprint, Response, request
from flask_cors import cross_origin
from jsonschema import validate
import jsonpickle
import json

from application.controller.dto.machine_state import MachineState
from application.controller.dto.machine_sensors import Sensors
from application.controller.dto.sensors.bioreactor_1_sensors import Bioreactor1Sensors
from application.controller.dto.sensors.bioreactor_2_sensors import Bioreactor2Sensors
from application.controller.dto.sensors.bsf_reproduction_sensors import BSFReproductionSensors
from application.controller.dto.sensors.shared_air_sensors import SharedAirSensors
from application.controller.dto.sensors.shredder_sensors import ShredderSensors
from application.controller.dto.actuators.actuator import Actuator
from application.controller.dto.actuators.options import Options
from application.controller.dto.actuators.type import Type
from application.model.action.action import Action
from application.model.action.action_set import ActionSet
from application.model.routine.advanced_tab_routine import AdvancedTabRoutine
from application.model.routine.routine_step import RoutineStep
from application.service.device_registry_service import DeviceRegistryService
from application.service.mcu_state_tracker_service import MCUStateTrackerService
from application.service.state_manager import StateManager


machineState = MachineState(
        [
            Actuator(
                "e0",
                str(Type.RADIO.name),
                "Rotary Valve 1",
                "1",
                [
                    Options("1", 1), 
                    Options("2", 2),
                    Options("3", 3),
                    Options("4", 4),
                    Options("5", 5),
                    Options("6", 6),
                ]
            ),
            Actuator(
                "e1",
                str(Type.RADIO.name),
                "Rotary Valve 2",
                "2",
                [
                    Options("1", 1), 
                    Options("2", 2),
                    Options("3", 3),
                    Options("4", 4),
                    Options("5", 5),
                    Options("6", 6),
                ]
            ),
            Actuator(
                "e2",
                str(Type.RADIO.name),
                "Rotary Valve 3",
                "3",
                [
                    Options("One", 1), 
                    Options("2", 2),
                    Options("3", 3),
                    Options("4", 4),
                    Options("5", 5),
                    Options("6", 6),
                ]
            ),
            Actuator(
                "eb",
                str(Type.RANGE.name),
                "Discrete Valve 1",
                "10",
                None,
                0,
                100,
                10,
                "Percent"
            ),
            Actuator(
                "ec",
                str(Type.RANGE.name),
                "Discrete Valve 2",
                "20",
                None,
                0,
                100,
                10,
                "Percent"
            ),
            Actuator(
                "f4",
                str(Type.RANGE.name),
                "Discrete Valve 3",
                "30",
                None,
                0,
                100,
                10,
                "Percent"
            ),
            Actuator(
                "e7",
                str(Type.SWITCH.name),
                "Flap Diverter Valve 1",
                "false"
            ),
            Actuator(
                "e8",
                str(Type.SWITCH.name),
                "Flap Diverter Valve 2",
                "true"
            ),
            Actuator(
                "ea",
                str(Type.SWITCH.name),
                "Flap Diverter Valve 3",
                "true"
            ),
            Actuator(
                "f1",
                str(Type.SWITCH.name),
                "Regen Blower",
                "true"
            ),
            Actuator(
                "f31",
                str(Type.SWITCH.name),
                "O3 Generator",
                "true"
            ),
            Actuator(
                "f41",
                str(Type.RANGE.name),
                "Blower Strength",
                "30",
                None,
                0,
                100,
                10,
                "Percent"
            ),
            Actuator(
                "ed",
                str(Type.SWITCH.name),
                "Shredder In Valve",
                "true"
            ),
            Actuator(
                "e3",
                str(Type.RANGE.name),
                "Shredder Out Valve",
                "90",
                None,
                0,
                100,
                10,
                "Percent"
            ),
            Actuator(
                "f32",
                str(Type.SWITCH.name),
                "Bioreactor 1 In Valve",
                "true"
            ),
            Actuator(
                "e4",
                str(Type.RANGE.name),
                "Bioreactor 1 Out Valve",
                "90",
                None,
                0,
                100,
                10,
                "Percent"
            ),
            Actuator(
                "f33",
                str(Type.SWITCH.name),
                "Bioreactor 2 In Valve",
                "true"
            ),
            Actuator(
                "e5",
                str(Type.RANGE.name),
                "Bioreactor 2 Out Valve",
                "90",
                None,
                0,
                100,
                10, 
                "Percent"
            ),
            Actuator(
                "f34",
                str(Type.SWITCH.name),
                "BSF Reproduction In Valve",
                "true"
            ),
            Actuator(
                "e6",
                str(Type.RANGE.name),
                "BSF Reproduction Out Valve",
                "90",
                None,
                0,
                100,
                10, 
                "Percent"
            ),
            Actuator(
                "f35",
                str(Type.SWITCH.name),
                "BSF Reproduction Light",
                "true"
            ),
        ],
        Sensors(
            SharedAirSensors(
                flowrate=50,
                o3=0.01,
            ),
            ShredderSensors(
                temperature=25.51,
                humidity=65.21,
                co2=5.68,
                pressure=1.68,
                h2=2.32,
            ),
            Bioreactor1Sensors(
                temperature=25.51,
                humidity=65.21,
                co2=5.68,
                pressure=1.68,
                h2=2.32,
            ),
            Bioreactor2Sensors(
                temperature=25.51,
                humidity=65.21,
                co2=5.68,
                pressure=1.68,
                h2=2.32,
            ),
            BSFReproductionSensors(
                temperature=25.51,
                humidity=65.21,
                co2=5.68,
                pressure=1.68,
                h2=2.32,
            )
        )
    )


def construct_mock_get_response():
    return machineState


def generate_routine_to_set_state(machine_state: MachineState,
                                  mcu_state_tracker_service: MCUStateTrackerService,
                                  device_registry_service: DeviceRegistryService) -> AdvancedTabRoutine:

    intended_actuator_states = {}
    for actuator in machine_state.actuators:
        intended_actuator_states[actuator.id] = actuator.value

    current_actuator_states = mcu_state_tracker_service.get_actuator_states()

    required_actions = []
    for device_id, intended_state_value in intended_actuator_states.items():

        device = device_registry_service.get_device(device_id)

        # Boolean values need to be true/false and not open/close and on/off
        if 'open' in device.possible_states.keys():
            intended_val = {'true': 'open', 'false': 'close'}.get(intended_state_value)
        elif 'on' in device.possible_states.keys():
            intended_val = {'true': 'on', 'false': 'off'}.get(intended_state_value)
        elif 'divert' in device.possible_states.keys():
            intended_val = {'true': 'divert', 'false': 'through'}.get(intended_state_value)
        else:
            intended_val = intended_state_value

        # Verify that the intended state is a possible state
        if intended_val not in device.possible_states.keys():
            raise RuntimeError(f"Cannot set state of {device.device_friendly_name} ({device_id}) to '{intended_val}' "
                               f"because the possible states are {list(device.possible_states.keys())}")

        if current_actuator_states.get(device_id, None) == intended_val:
            continue

        required_actions.append(Action(device_id, intended_val))

    routine = AdvancedTabRoutine(steps=[
        RoutineStep(ActionSet(iterable=required_actions), then_wait_n_sec=0)
    ])

    return routine


def convert_mcu_state_to_response(mcu_state_tracker_service: MCUStateTrackerService,
                                  device_registry_service: DeviceRegistryService):

    actuators = []
    for device_id, state_value in mcu_state_tracker_service.get_actuator_states().items():

        device = device_registry_service.get_device(device_id)

        # Boolean values need to be true/false and not open/close and on/off
        remap_state_value = {
            'open': 'true',
            'close': 'false',
            'on': 'true',
            'off': 'false',
            'divert': 'true',
            'through': 'false',
        }
        val = remap_state_value.get(state_value, state_value)

        display_type = Type.SWITCH
        if device.device_type_name in [
            'RotaryDiverterValve1To6',
            'RotaryDiverterValve6To1'
        ]:
            display_type = Type.RADIO
        elif device.device_type_name == 'DiscreteFlapDiverterValve':
            display_type = Type.RANGE

        options = min = max = step = unit = None
        if display_type == Type.RADIO:
            options = []
            for string_value in device.possible_states.keys():
                options.append(Options(string_value, int(string_value)))
        elif display_type == Type.RANGE:
            # Hard coding this because this only works for the flap diverter valve.
            min = 0
            max = 100
            step = 5
            unit = 'percent'

        actuators.append(Actuator(
                device_id,
                str(display_type.name),
                device.device_friendly_name,
                val,
                options,
                min,
                max,
                step,
                unit
            ))

    shared_air_sensors = SharedAirSensors(**{
        measurement_name: float(value) if value is not None else None
        for measurement_name, value
        in mcu_state_tracker_service.get_latest_measurements()['AirLoop'].items()
        })
    shredder_storage_sensors = ShredderSensors(**{
        measurement_name: float(value) if value is not None else None
        for measurement_name, value
        in mcu_state_tracker_service.get_latest_measurements()['ShredderStorage'].items()
        })
    bioreactor_1_sensors = Bioreactor1Sensors(**{
        measurement_name: float(value) if value is not None else None
        for measurement_name, value
        in mcu_state_tracker_service.get_latest_measurements()['Bioreactor1'].items()
        })
    bioreactor_2_sensors = Bioreactor2Sensors(**{
        measurement_name: float(value) if value is not None else None
        for measurement_name, value
        in mcu_state_tracker_service.get_latest_measurements()['Bioreactor2'].items()
        })
    bsf_reproduction_sensors = BSFReproductionSensors(**{
        measurement_name: float(value) if value is not None else None
        for measurement_name, value
        in mcu_state_tracker_service.get_latest_measurements()['BSFReproduction'].items()
        })

    machine_state = MachineState(actuators,
                                 Sensors(
                                     shared_air_sensors,
                                     shredder_storage_sensors,
                                     bioreactor_1_sensors,
                                     bioreactor_2_sensors,
                                     bsf_reproduction_sensors
                                     )
                                 )
    return machine_state


# Dynamically generate blueprint for dependency injection. Classes aren't supported due to Flask limitations.
def construct_state_bp(state_manager: StateManager,
                       mcu_state_tracker_service: MCUStateTrackerService,
                       device_registry_service: DeviceRegistryService):
    state_bp = Blueprint('state', __name__)

    # state REST endpoint supporting GET & POST
    @state_bp.route('/state', methods=['GET', 'POST'])
    @cross_origin(supports_credentials=True)
    def state():
        if request.method == 'POST':
            try:
                validate(request.get_json(), schema=MachineState.get_schema())
                machine_state = jsonpickle.decode(json.dumps(request.get_json()))
                routine = generate_routine_to_set_state(machine_state, mcu_state_tracker_service, device_registry_service)
                state_manager.add_routine_to_queue(routine)
                return Response(json.dumps({"result": "success!"}), status=200)
                # global machineState
                # machineState = jsonpickle.decode(json.dumps(request.get_json()))
                # return Response(json.dumps({"result": "success!"}), status=200)
            except Exception as e:
                print("Schema failed validation: {}", str(e))
                return Response(json.dumps({"error": str(e)}), status=400)
        elif request.method == 'GET':
            machine_state = convert_mcu_state_to_response(mcu_state_tracker_service, device_registry_service)
            return Response(jsonpickle.encode(machine_state), status=200)
            # return Response(jsonpickle.encode(construct_mock_get_response()), status=200)

    return state_bp
