import logging

from flask import Blueprint, Response, request
from flask_cors import cross_origin
from jsonschema import validate
import jsonpickle
import json

from application.controller.dto.routine import Routine
from application.controller.dto.task import Task
from application.controller.dto.task_queue import TaskQueue
from application.service.isolation_state_registry_service import IsolationStateRegistryService
from application.service.routine_registry_service import RoutineRegistryService
from application.service.state_manager import StateManager


# Dynamically generate blueprint for dependency injection. Classes aren't supported due to Flask limitations.
def construct_task_queue_bp(state_manager: StateManager, routines_service: RoutineRegistryService,
                            isolation_state_registry_service: IsolationStateRegistryService):
    task_queue_bp = Blueprint('task_queue', __name__)

    # task_queue REST endpoint supporting GET & POST
    @task_queue_bp.route('/task_queue', methods=['GET', 'POST'])
    @cross_origin(supports_credentials=True)
    def task_queue():

        if request.method == 'POST':

            try:
                validate(request.get_json(), schema=TaskQueue.get_schema())
                task_queue_dto: TaskQueue = jsonpickle.decode(json.dumps(request.get_json()))

            except Exception as e:
                logging.error(f"Schema validation failed: {e}")
                return Response(json.dumps({"error": str(e)}), status=400)

            for task in task_queue_dto.tasks:

                try:
                    routine_dto: Routine = task.routine

                    routine_model = routines_service.get_routine(routine_dto.name)

                    # TODO - make less ugly, and move this logic to the translator service once that branch is merged
                    isolation_state_model = None
                    isolation_state_required = routine_model.must_run_in_state
                    if isolation_state_required is not None:
                        isolation_state_model = isolation_state_registry_service.get_isolation_state(
                            isolation_state_required.name)

                    if state_manager.routines_currently_disabled:
                        err = f"Cannot run the {routine_model.name} routine because routine running is disabled " \
                              f"between {state_manager.disable_routines_between[0]} and " \
                              f"{state_manager.disable_routines_between[1]}"
                        return Response(json.dumps({"error": err}), status=400)

                    state_manager.add_routine_to_queue(routine_model, isolation_state_model)

                except Exception as e:
                    logging.error(f"Failed to add routine to queue: {e}")
                    return Response(json.dumps({"error": str(e)}), status=400)

            return Response(json.dumps({"result": "success!"}), status=200)

        elif request.method == 'GET':

            if state_manager.currently_running_routine is not None:
                current_routine = Routine(state_manager.currently_running_routine.name)
            else:
                current_routine = None

            task_queue_dto = TaskQueue(
                current_routine,
                [
                    Task(Routine(task.routine.name))
                    for task
                    in state_manager.current_task_queue
                ]
            )

            return Response(jsonpickle.encode(task_queue_dto), status=200)

    return task_queue_bp
