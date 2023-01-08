#!/bin/bash

# In another terminal, watch the task queue:
# watch -n 1 -c "curl -s -X GET http://127.0.0.1:5000/task_queue -H 'Content-Type: application/json' | python -m json.tool"

# Then add some tasks to the queue and make sure it works
curl -X POST http://127.0.0.1:5000/task_queue -H 'Content-Type: application/json' -d '{
    "py/object": "application.controller.dto.task_queue.TaskQueue",
    "tasks": [
        {
            "py/object": "application.controller.dto.task.Task",
            "routine": {
                "py/object": "application.controller.dto.routine.Routine",
                "name": "HumidifyBioreactor1Routine"
            }
        }
    ]
}'

sleep 3

curl -X POST http://127.0.0.1:5000/meta_state -H 'Content-Type: application/json' -d '{
    "py/object": "application.controller.dto.system_meta_state.SystemMetaState",
    "disable_automated_routines": true
}'

