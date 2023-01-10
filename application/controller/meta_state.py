from flask import Blueprint, Response, request
from flask_cors import cross_origin
from jsonschema import validate
import jsonpickle
import json

from application.controller.dto.system_meta_state import SystemMetaState
from application.service.state_manager import StateManager


# Dynamically generate blueprint for dependency injection. Classes aren't supported due to Flask limitations.
def construct_meta_state_bp(state_manager: StateManager):
    meta_state_bp = Blueprint('meta_state', __name__)

    # meta_state REST endpoint supporting GET & POST
    @meta_state_bp.route('/meta_state', methods=['GET', 'POST'])
    @cross_origin(supports_credentials=True)
    def meta_state():

        if request.method == 'POST':

            try:
                validate(request.get_json(), schema=SystemMetaState.get_schema())
            except Exception as e:
                print("Schema failed validation: {}", str(e))
                return Response(json.dumps({"error": str(e)}), status=400)

            system_meta_state: SystemMetaState = jsonpickle.decode(json.dumps(request.get_json()))

            if system_meta_state.disable_automated_routines:
                state_manager.disable_automated_routine_running()
            elif not system_meta_state.disable_automated_routines:
                state_manager.enable_automated_routine_running()

            return Response(json.dumps({"result": "success!"}), status=200)

        elif request.method == 'GET':

            # This is too basic to bother with a translator service
            system_meta_state = SystemMetaState(disable_automated_routines=state_manager.automated_routines_disabled)
            return Response(jsonpickle.encode(system_meta_state), status=200)

    return meta_state_bp
