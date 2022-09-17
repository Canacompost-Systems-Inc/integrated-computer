from flask import Blueprint, Response, request
from flask_cors import cross_origin
import json

from application.service.oxygen import *

# Construct a GET response model. 
def construct_get_response(result):
    return json.dumps({"value": result})

# Dynamically generate blueprint for dependency injection. Classes aren't supported due to Flask limitations.
def construct_oxygen_bp(oxygen_service):
    oxygen_bp = Blueprint('oxygen', __name__)

    # Oxygen REST endpoint supporting GET & POST
    @oxygen_bp.route('/oxygen', methods=['GET', 'POST'])
    @cross_origin(supports_credentials=True)
    def oxygen():
        if request.method == 'POST':
            result = oxygen_service.setOxygen(int(request.get_json().get("value")))
            return Response(result, status=200)
        elif request.method == 'GET':
            result = oxygen_service.getOxygen()
            return Response(construct_get_response(result), status=200)
        return Response("Bad request type", status=400)

    return(oxygen_bp)