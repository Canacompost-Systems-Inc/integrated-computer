from application.controller.schema.utils import get_schema_from_file


class TaskQueue:

    @staticmethod
    def get_schema():
        return get_schema_from_file('task_queue.json')

    def __init__(self, currently_running_routine, tasks):
        self.currently_running_routine = currently_running_routine
        self.tasks = tasks
