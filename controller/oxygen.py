from flask import Blueprint, Response, request
from service.oxygen import *
from flask_cors import cross_origin
import json

# Construct a GET response model. 
# TODO: Convert the result in a meaningful way. Right now we just return mock data 
def construct_get_response(result):
    return json.dumps({"value": "21%", "delta": "-2%"})

# Dynamically generate blueprint for dependency injection. Classes aren't supported due to Flask limitations.
def construct_oxygen_bp(oxygen_service):
    oxygen_bp = Blueprint('oxygen', __name__)

    # Oxygen REST endpoint supporting GET & POST
    @oxygen_bp.route('/oxygen', methods=['GET', 'POST'])
    @cross_origin(supports_credentials=True)
    def oxygen():
        match request.method: 
            case 'POST':
                result = oxygen_service.setOxygen(80)
                return Response(result, status=200)
            case 'GET': 
                result = oxygen_service.getOxygen()
                return Response(construct_get_response(result), status=200)
        return Response("Bad request type", status=400)

    return(oxygen_bp)