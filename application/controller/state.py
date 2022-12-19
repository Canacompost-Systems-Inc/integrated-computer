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
from flask import Blueprint, Response, request
from flask_cors import cross_origin
from jsonschema import validate
import jsonpickle
import json

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
                    Options("1", 1), 
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
                "f3",
                str(Type.SWITCH.name),
                "O3 Generator",
                "true"
            ),
            Actuator(
                "f4",
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
                "f3",
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
                "f3",
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
                "f3",
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
                "f3",
                str(Type.SWITCH.name),
                "BSF Reproduction Light",
                "true"
            ),
        ],
        Sensors(
            SharedAirSensors(
                pressure=50
            ),
            ShredderSensors(
                humidity=30,
                c02=5,
                air_temperature=18,
                soil_temperature=20
            ),
            Bioreactor1Sensors(
                humidity=30,
                c02=5,
                air_temperature=18,
                soil_temperature=20
            ),
            Bioreactor2Sensors(
                humidity=30,
                c02=5,
                air_temperature=18,
                soil_temperature=20
            ),
            BSFReproductionSensors(
                humidity=30,
                c02=5,
                air_temperature=18,
                soil_temperature=20
            )
        )
    )

def construct_mock_get_response():
    return machineState

# Dynamically generate blueprint for dependency injection. Classes aren't supported due to Flask limitations.
def construct_state_bp():
    state_bp = Blueprint('state', __name__)

    # state REST endpoint supporting GET & POST
    @state_bp.route('/state', methods=['GET', 'POST'])
    @cross_origin(supports_credentials=True)
    def state():
        if request.method == 'POST':
            try:
                validate(request.get_json(), schema=MachineState.get_schema())
                global machineState 
                machineState = jsonpickle.decode(json.dumps(request.get_json()))
                return Response(json.dumps({"result": "success!"}), status=200)
            except Exception as e:
                print("Schema failed validation: {}", str(e))
                return Response(json.dumps({"error": str(e)}), status=400)
        elif request.method == 'GET':
            return Response(jsonpickle.encode(construct_mock_get_response()), status=200)

    return (state_bp)
