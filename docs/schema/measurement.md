# Measurement Schema

Used to get the measurement units and expected ranges. Supports GET.

### JSON Schema

```json
{
    "type": "object",
    "properties": {
        "measurements": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": { "type": "string" },
                    "unit": { "type": "string" },
                    "min": { "type": "number" },
                    "max": { "type": "number" },
                    "idealMin": { "type": "number" },
                    "idealMax": { "type": "number" }
                },
                "required": ["name", "unit", "min", "max", "idealMin", "idealMax"]
            }
        }
    }
}
```

### Examples

```console
user@local:~$ curl -X GET http://127.0.0.1:5000/measurement -H 'Content-Type: application/json' | python -m json.tool
{
    "py/object": "application.controller.dto.measurements.Measurements",
    "measurements": [
        {
            "py/object": "application.controller.dto.measurement.Measurement",
            "name": "co2",
            "unit": "ppm",
            "min": 400.0,
            "max": 5000.0,
            "idealMin": 400.0,
            "idealMax": 1000.0
        },
        {
            "py/object": "application.controller.dto.measurement.Measurement",
            "name": "flowrate",
            "unit": "L/min",
            "min": 0.0,
            "max": 30.0,
            "idealMin": 0.0,
            "idealMax": 20.0
        },
        {
            "py/object": "application.controller.dto.measurement.Measurement",
            "name": "h2",
            "unit": "ppm",
            "min": 0.0,
            "max": 50.0,
            "idealMin": 0.0,
            "idealMax": 25.0
        },
        {
            "py/object": "application.controller.dto.measurement.Measurement",
            "name": "humidity",
            "unit": "%",
            "min": 0.0,
            "max": 100.0,
            "idealMin": 0.0,
            "idealMax": 50.0
        },
        {
            "py/object": "application.controller.dto.measurement.Measurement",
            "name": "o3",
            "unit": "ppb",
            "min": 0.0,
            "max": 100.0,
            "idealMin": 0.0,
            "idealMax": 20.0
        },
        {
            "py/object": "application.controller.dto.measurement.Measurement",
            "name": "pressure",
            "unit": "Pa",
            "min": 95000.0,
            "max": 105000.0,
            "idealMin": 100000.0,
            "idealMax": 101000.0
        },
        {
            "py/object": "application.controller.dto.measurement.Measurement",
            "name": "temperature",
            "unit": "C",
            "min": 0.0,
            "max": 65.0,
            "idealMin": 0.0,
            "idealMax": 30.0
        },
        {
            "py/object": "application.controller.dto.measurement.Measurement",
            "name": "state",
            "unit": "",
            "min": 0.0,
            "max": 0.0,
            "idealMin": 0.0,
            "idealMax": 0.0
        }
    ]
}
```
