from flask import Blueprint, Response, request
from flask_cors import cross_origin
import jsonpickle

from application.controller.dto.routine import Routine
from application.controller.dto.routines import Routines
from application.service.routine_registry_service import RoutineRegistryService


# Dynamically generate blueprint for dependency injection. Classes aren't supported due to Flask limitations.
def construct_routine_bp(routines_service: RoutineRegistryService):
    routine_bp = Blueprint('routine', __name__)

    # routine REST endpoint supporting GET
    @routine_bp.route('/routine', methods=['GET'])
    @cross_origin(supports_credentials=True)
    def routine():

        if request.method == 'GET':

            # Too simple to bother with a translator service
            routines = Routines(
                Routine(_routine.name)
                for _routine
                in routines_service.all_routines()
            )

            return Response(jsonpickle.encode(routines), status=200)

    return routine_bp
