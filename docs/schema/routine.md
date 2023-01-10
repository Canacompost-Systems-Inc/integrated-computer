# Routine Schema

Used to get the routines that can be run in the system. Supports GET.

### JSON Schema

```json
{
    "type": "object",
    "properties": {
        "routines": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": { "type": "string" }
                },
                "required": ["name"]
            }
        }
    }
}
```

### Examples

```console
user@local:~$ curl -X GET http://127.0.0.1:5000/routine -H 'Content-Type: application/json' | python -m json.tool
{
    "py/object": "application.controller.dto.routines.Routines",
    "routines": [
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "CoolAndDehumidifyBioreactor1Routine"
        },
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "CoolAndDehumidifyBioreactor2Routine"
        },
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "CoolAndDehumidifyBSFReproductionRoutine"
        },
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "CoolAndDehumidifyShredderStorageRoutine"
        },
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "CoolAndDehumidifySieveRoutine"
        },
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "FlushAirLoopRoutine"
        },
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "FlushCompostLoopRoutine"
        },
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "HeatBioreactor1Routine"
        },
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "HeatBioreactor2Routine"
        },
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "HeatBSFReproductionRoutine"
        },
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "HeatShredderStorageRoutine"
        },
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "HumidifyBioreactor1Routine"
        },
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "HumidifyBioreactor2Routine"
        },
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "HumidifyBSFReproductionRoutine"
        },
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "HumidifyShredderStorageRoutine"
        },
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "MoveCompostFromBioreactor1ToBSFReproductionRoutine"
        },
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "MoveCompostFromBioreactor1ToShredderStorageRoutine"
        },
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "MoveCompostFromBioreactor2ToBSFReproductionRoutine"
        },
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "MoveCompostFromBioreactor2ToShredderStorageRoutine"
        },
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "MoveCompostFromBSFReproductionToBioreactor1Routine"
        },
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "MoveCompostFromBSFReproductionToBioreactor2Routine"
        },
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "MoveCompostFromBSFReproductionToSieveRoutine"
        },
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "MoveCompostFromShredderStorageToBioreactor1Routine"
        },
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "MoveCompostFromShredderStorageToBioreactor2Routine"
        },
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "ReadSensorsBioreactor1Routine"
        },
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "ReadSensorsBioreactor2Routine"
        },
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "ReadSensorsBSFReproductionRoutine"
        },
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "ReadSensorsShredderStorageRoutine"
        },
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "ReadSensorsSieveRoutine"
        },
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "SanitizeAirLoopRoutine"
        },
        {
            "py/object": "application.controller.dto.routine.Routine",
            "name": "SanitizeCompostLoopRoutine"
        }
    ]
}
```
