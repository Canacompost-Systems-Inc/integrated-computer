from flask import Blueprint, Response, jsonify, request
from service.temperature import *
from flask_cors import cross_origin
import json

# Construct a GET response model. 
# TODO: Convert the result in a meaningful way. Right now we just return mock data 
def construct_get_response(result):
    return json.dumps({"value": "25C", "delta": "+4C"})

# Dynamically generate blueprint for dependency injection. Classes aren't supported due to Flask limitations.
def construct_temperature_bp(temperature_service):
    temperature_bp = Blueprint('temperature', __name__)

    # temperature REST endpoint supporting GET & POST
    @temperature_bp.route('/temperature', methods=['GET', 'POST'])
    @cross_origin(supports_credentials=True)
    def temperature():
        match request.method: 
            case 'POST':
                result = temperature_service.setTemperature(80)
                return Response(result, status=200)
            case 'GET': 
                result = temperature_service.getTemperature()
                return Response(construct_get_response(result), status=200)
        return Response("Bad request type", status=400)

    return(temperature_bp)