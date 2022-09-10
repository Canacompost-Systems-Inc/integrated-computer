from flask import Blueprint, Response, jsonify, request
from flask_cors import cross_origin
import json

from application.service.temperature import *

# Construct a GET response model. 
def construct_get_response(result):
    return json.dumps({"value": result})

# Dynamically generate blueprint for dependency injection. Classes aren't supported due to Flask limitations.
def construct_temperature_bp(temperature_service):
    temperature_bp = Blueprint('temperature', __name__)

    # temperature REST endpoint supporting GET & POST
    @temperature_bp.route('/temperature', methods=['GET', 'POST'])
    @cross_origin(supports_credentials=True)
    def temperature():
        if request.method == 'POST':
            result = temperature_service.setTemperature(int(request.get_json().get("value")))
            return Response(result, status=200)
        elif request.method == 'GET':
            result = temperature_service.getTemperature()
            return Response(construct_get_response(result), status=200)
        return Response("Bad request type", status=400)

    return(temperature_bp)