# Task Queue Schema

Used to get the currently running routine and the task queue, and for adding new tasks to the queue. Supports GET and POST.

### JSON Schema

```json
{
    "type": "object",
    "properties": {
        "currently_running_routine": {
            "type": ["object", "null"],
            "properties": {
                "name": {"type": "string"}
            }
        },
        "tasks": {
            "type": ["array", "null"],
            "items": {
                "type": ["object", "null"],
                "properties": {
                    "routine": {
                        "type": ["object", "null"],
                        "properties": {
                            "name": {"type": "string"}
                        },
                        "required": ["name"]
                    }
                }
            }
        }
    }
}
```

### Examples

```console
user@local:~$ curl -X GET http://127.0.0.1:5000/task_queue -H 'Content-Type: application/json' | python -m json.tool
{
    "py/object": "application.controller.dto.task_queue.TaskQueue",
    "currently_running_routine": null,
    "tasks": []
}

user@local:~$ curl -X GET http://127.0.0.1:5000/task_queue -H 'Content-Type: application/json' | python -m json.tool
{
    "py/object": "application.controller.dto.task_queue.TaskQueue",
    "currently_running_routine": {
        "py/object": "application.controller.dto.routine.Routine",
        "name": "FlushAirLoopRoutine"
    },
    "tasks": [
        {
            "py/object": "application.controller.dto.task.Task",
            "routine": {
                "py/object": "application.controller.dto.routine.Routine",
                "name": "ReadSensorsBioreactor1Routine"
            }
        }
    ]
}

user@local:~$ curl -X POST http://127.0.0.1:5000/task_queue -H 'Content-Type: application/json' -d '{
    "py/object": "application.controller.dto.task_queue.TaskQueue",
    "tasks": [
        {
            "py/object": "application.controller.dto.task.Task",
            "routine": {
                "py/object": "application.controller.dto.routine.Routine",
                "name": "ReadSensorsBioreactor1Routine"
            }
        }
    ]
}'
{"result": "success!"}
```
