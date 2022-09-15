from flask import Blueprint, Response, request
from flask_cors import cross_origin

from application.service.routines import *

# Dynamically generate blueprints for dependency injection. Classes aren't supported due to Flask limitations.
def construct_r0_bp(routines):
    r0_bp = Blueprint('r0', __name__)

    # r0 REST endpoint supporting GET & POST
    # TODO: Remove GET. Right now it is useful for easy browser testing
    @r0_bp.route('/r0', methods=['GET', 'POST'])
    @cross_origin(supports_credentials=True)
    def r0():
        if request.method == 'POST':
            result = routines.startR0()
            return Response(result, status=200)
        elif request.method == 'GET':
            result = routines.startR0()
            return Response(status=200)
        return Response("Bad request type", status=400)

    return(r0_bp)

def construct_r1_bp(routines):
    r1_bp = Blueprint('r1', __name__)

    # r1 REST endpoint supporting GET & POST
    # TODO: Remove GET. Right now it is useful for easy browser testing
    @r1_bp.route('/r1', methods=['GET', 'POST'])
    @cross_origin(supports_credentials=True)
    def r1():
        if request.method == 'POST':
            result = routines.startR1()
            return Response(result, status=200)
        elif request.method == 'GET':
            result = routines.startR1()
            return Response(status=200)
        return Response("Bad request type", status=400)

    return(r1_bp)

def construct_r2_bp(routines):
    r2_bp = Blueprint('r2', __name__)

    # r2 REST endpoint supporting GET & POST
    # TODO: Remove GET. Right now it is useful for easy browser testing
    @r2_bp.route('/r2', methods=['GET', 'POST'])
    @cross_origin(supports_credentials=True)
    def r2():
        if request.method == 'POST':
            result = routines.startR2()
            return Response(result, status=200)
        elif request.method == 'GET':
            result = routines.startR2()
            return Response(status=200)
        return Response("Bad request type", status=400)

    return(r2_bp)

def construct_r3_bp(routines):
    r3_bp = Blueprint('r3', __name__)

    # r3 REST endpoint supporting GET & POST
    # TODO: Remove GET. Right now it is useful for easy browser testing
    @r3_bp.route('/r3', methods=['GET', 'POST'])
    @cross_origin(supports_credentials=True)
    def r3():
        if request.method == 'POST':
            result = routines.startR3()
            return Response(result, status=200)
        elif request.method == 'GET':
            result = routines.startR3()
            return Response(status=200)
        return Response("Bad request type", status=400)

    return(r3_bp)

def construct_r4_bp(routines):
    r4_bp = Blueprint('r4', __name__)

    # r4 REST endpoint supporting GET & POST
    # TODO: Remove GET. Right now it is useful for easy browser testing
    @r4_bp.route('/r4', methods=['GET', 'POST'])
    @cross_origin(supports_credentials=True)
    def r4():
        if request.method == 'POST':
            result = routines.startR4()
            return Response(result, status=200)
        elif request.method == 'GET':
            result = routines.startR4()
            return Response(status=200)
        return Response("Bad request type", status=400)

    return(r4_bp)

def construct_r5_bp(routines):
    r5_bp = Blueprint('r5', __name__)

    # r5 REST endpoint supporting GET & POST
    # TODO: Remove GET. Right now it is useful for easy browser testing
    @r5_bp.route('/r5', methods=['GET', 'POST'])
    @cross_origin(supports_credentials=True)
    def r5():
        if request.method == 'POST':
            result = routines.startR5()
            return Response(result, status=200)
        elif request.method == 'GET':
            result = routines.startR5()
            return Response(status=200)
        return Response("Bad request type", status=400)

    return(r5_bp)