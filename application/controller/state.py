from flask import Blueprint, Response, request
from flask_cors import cross_origin
from jsonschema import validate
import jsonpickle
import json

from application.controller.dto.machine_state import MachineState
from application.service.dto_translator_service import DtoTranslatorService
from application.service.mcu_state_tracker_service import MCUStateTrackerService
from application.service.state_manager import StateManager


# Dynamically generate blueprint for dependency injection. Classes aren't supported due to Flask limitations.
def construct_state_bp(state_manager: StateManager,
                       mcu_state_tracker_service: MCUStateTrackerService,
                       dto_translator_service: DtoTranslatorService):
    state_bp = Blueprint('state', __name__)

    # state REST endpoint supporting GET & POST
    @state_bp.route('/state', methods=['GET', 'POST'])
    @cross_origin(supports_credentials=True)
    def state():
        if request.method == 'POST':

            try:
                validate(request.get_json(), schema=MachineState.get_schema())
                machine_state = jsonpickle.decode(json.dumps(request.get_json()))
            except Exception as e:
                print("Schema failed validation: {}", str(e))
                return Response(json.dumps({"error": str(e)}), status=400)

            routine = dto_translator_service.generate_routine_to_set_actuator_state(
                mcu_state_tracker_service.get_actuator_states(),
                machine_state
            )
            if routine is not None:
                if not state_manager.automated_routines_disabled:
                    return Response(json.dumps({"error": f"Cannot run routine to set actuator states manually because "
                                                         f"automated routine running has not been disabled"}),
                                    status=400)

                state_manager.add_routine_to_queue(routine, to_start=True)

            return Response(json.dumps({"result": "success!"}), status=200)

        elif request.method == 'GET':

            machine_state = dto_translator_service.construct_machine_state_dto(
                mcu_state_tracker_service.get_actuator_states(),
                mcu_state_tracker_service.get_latest_measurements()
            )
            return Response(jsonpickle.encode(machine_state), status=200)

    return state_bp
