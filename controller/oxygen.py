from flask import Blueprint, Response, request
from service.oxygen import *

# Dynamically generate blueprint for dependency injection. Classes aren't supported due to Flask limitations.
def construct_oxygen_bp(oxygen_service):
    oxygen_bp = Blueprint('oxygen', __name__)

    # Oxygen REST endpoint supporting GET & POST
    @oxygen_bp.route('/oxygen', methods=['GET'])
    def oxygen():
        match request.method: 
            case 'POST':
                result = oxygen_service.setOxygen(80)
                return Response(result, status=200)
            case 'GET': 
                result = oxygen_service.getOxygen()
                return Response(result, status=200)
        return Response("Bad request type", status=400)

    return(oxygen_bp)