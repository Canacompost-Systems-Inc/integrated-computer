import json
from pathlib import Path


def get_schema_from_file(schema_file_name: str):
    schema_dir = Path(__file__).parent

    for child in schema_dir.iterdir():

        if child.name == schema_file_name:

            with open(child) as f:
                return json.load(f)

    raise RuntimeError(f"Could not locate schema file {schema_file_name} in {schema_dir}")
