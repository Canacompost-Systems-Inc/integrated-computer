from flask import Blueprint, Response, request
from flask_cors import cross_origin
import jsonpickle

from application.controller.dto.measurement import Measurement
from application.controller.dto.measurements import Measurements
from application.service.measurement_factory import MeasurementFactory


# Dynamically generate blueprint for dependency injection. Classes aren't supported due to Flask limitations.
def construct_measurement_bp(measurement_factory: MeasurementFactory):
    measurement_bp = Blueprint('measurement', __name__)

    # measurement REST endpoint supporting GET
    @measurement_bp.route('/measurement', methods=['GET'])
    @cross_origin(supports_credentials=True)
    def measurement():

        if request.method == 'GET':

            # Too simple to bother with a translator service
            measurements = Measurements([
                Measurement(
                    _measurement_name,
                    measurement_factory.get_measurement(_measurement_name, 0).unit,
                    measurement_factory.get_measurement(_measurement_name, 0).normal_min,
                    measurement_factory.get_measurement(_measurement_name, 0).normal_max,
                    measurement_factory.get_measurement(_measurement_name, 0).ideal_min,
                    measurement_factory.get_measurement(_measurement_name, 0).ideal_max,
                )
                for _measurement_name
                in measurement_factory.available_measurements
            ])

            return Response(jsonpickle.encode(measurements), status=200)

    return measurement_bp
