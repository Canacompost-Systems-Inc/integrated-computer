# Meta State Schema

Used to set the meta-state of the system, as opposed to the state of the actuators/sensors. Supports GET and POST.

When setting disable_automated_routines to false, the system will continue running any currently running routine or state change routines, but will not run anything from the task queue. This does not prevent the state API used for the advanced tab from working.

### JSON Schema

```json
{
    "type": "object",
    "properties": {
        "disable_automated_routines": { "type": "boolean" }
    },
    "required": [
        "disable_automated_routines"
    ]
}
```

### Examples

```console
user@local:~$ curl -X GET http://127.0.0.1:5000/meta_state -H 'Content-Type: application/json' | python -m json.tool
{
    "py/object": "application.controller.dto.system_meta_state.SystemMetaState",
    "disable_automated_routines": false
}

user@local:~$ curl -X POST http://127.0.0.1:5000/meta_state -H 'Content-Type: application/json' -d '{
    "py/object": "application.controller.dto.system_meta_state.SystemMetaState",
    "disable_automated_routines": true
}'
{"result": "success!"}
```
