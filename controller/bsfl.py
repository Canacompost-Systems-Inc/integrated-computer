from flask import Blueprint, Response, request
from service.bsfl import *
from flask_cors import cross_origin
from distutils import util
import json

# Construct a GET response model. 
def construct_get_response(result):
    return json.dumps({"value": result})

# Dynamically generate blueprint for dependency injection. Classes aren't supported due to Flask limitations.
def construct_bsfl_bp(bsfl_service):
    bsfl_bp = Blueprint('bsfl', __name__)

    # bsfl REST endpoint supporting GET & POST
    @bsfl_bp.route('/bsfl', methods=['GET', 'POST'])
    @cross_origin(supports_credentials=True)
    def bsfl():
        match request.method: 
            case 'POST':
                val = request.get_json().get("value") == "True" # Hack to convert string into boolean
                result = bsfl_service.setBSFL(val)
                return Response(result, status=200)
            case 'GET': 
                result = bsfl_service.getBSFL()
                return Response(construct_get_response(result), status=200)
        return Response("Bad request type", status=400)

    return(bsfl_bp)