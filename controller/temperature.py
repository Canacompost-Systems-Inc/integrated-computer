from flask import Blueprint, Response, request
from service.temperature import *

# Dynamically generate blueprint for dependency injection. Classes aren't supported due to Flask limitations.
def construct_temperature_bp(temperature_service):
    temperature_bp = Blueprint('temperature', __name__)

    # temperature REST endpoint supporting GET & POST
    @temperature_bp.route('/temperature', methods=['GET'])
    def temperature():
        match request.method: 
            case 'POST':
                result = temperature_service.setTemperature(80)
                return Response(result, status=200)
            case 'GET': 
                result = temperature_service.getTemperature()
                return Response(result, status=200)
        return Response("Bad request type", status=400)

    return(temperature_bp)