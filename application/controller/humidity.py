from flask import Blueprint, Response, request
from flask_cors import cross_origin
import json

from application.service.humidity import *

# Construct a GET response model. 
def construct_get_response(result):
    return json.dumps({"value": result})

# Dynamically generate blueprint for dependency injection. Classes aren't supported due to Flask limitations.
def construct_humidity_bp(humidity_service):
    humidity_bp = Blueprint('humidity', __name__)

    # humidity REST endpoint supporting GET & POST
    @humidity_bp.route('/humidity', methods=['GET', 'POST'])
    @cross_origin(supports_credentials=True)
    def humidity():
        if request.method == 'POST':
            result = humidity_service.setHumidity(int(request.get_json().get("value")))
            return Response(result, status=200)
        elif request.method == 'GET':
            result = humidity_service.getHumidity()
            return Response(construct_get_response(result), status=200)
        return Response("Bad request type", status=400)

    return(humidity_bp)