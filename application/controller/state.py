from application.controller.dto.machine_state import MachineState
from application.controller.dto.machine_actuators import Actuators
from application.controller.dto.machine_sensors import Sensors
from application.controller.dto.sensors.bioreactor_1_sensors import Bioreactor1Sensors
from application.controller.dto.sensors.bioreactor_2_sensors import Bioreactor2Sensors
from application.controller.dto.sensors.bsf_reproduction_sensors import BSFReproductionSensors
from application.controller.dto.sensors.shared_air_sensors import SharedAirSensors
from application.controller.dto.sensors.shredder_sensors import ShredderSensors
from application.controller.dto.actuators.bioreactor_1_actuators import Bioreactor1Actuators
from application.controller.dto.actuators.bioreactor_2_actuators import Bioreactor2Actuators
from application.controller.dto.actuators.bsf_reproduction_actuators import BSFReproductionActuators
from application.controller.dto.actuators.shared_air_actuators import SharedAirActuators
from application.controller.dto.actuators.shredder_actuators import ShredderActuators
from flask import Blueprint, Response, request
from flask_cors import cross_origin
from jsonschema import validate
import jsonpickle
import json

def construct_mock_get_response():
    return MachineState(
        Actuators(
            SharedAirActuators(
                rotary_valve_1=1,
                rotary_valve_2=2,
                rotary_valve_3=3,
                discrete_valve_1=10,
                discrete_valve_2=20,
                discrete_valve_3=30,
                flap_valve_1=True,
                flap_valve_2=False,
                flap_valve_3=True,
                blower_on=True,
                o3_generator=True,
                blower_strength=50,
            ),
            ShredderActuators(
                out_valve=True,
                in_valve=False
            ),
            Bioreactor1Actuators(
                out_valve=True,
                in_valve=False
            ),
            Bioreactor2Actuators(
                out_valve=True,
                in_valve=False
            ),
            BSFReproductionActuators(
                out_valve=True,
                in_valve=False,
                light=True
            )
        ),
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
                return Response(json.dumps({"result": "success!"}), status=200)
            except Exception as e:
                print("Schema failed validation: {}", str(e))
                return Response(json.dumps({"error": str(e)}), status=400)
        elif request.method == 'GET':
            return Response(jsonpickle.encode(construct_mock_get_response()), status=200)

    return (state_bp)
