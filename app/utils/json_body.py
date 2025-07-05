from flask import request
from typing import Any
from app.application.exceptions import BadRequestError

def get_valid_json_body() -> dict[str, Any]:
    json_data = request.get_json(silent=True)
    if not isinstance(json_data, dict):
        raise BadRequestError("Invalid or missing JSON body")
    return json_data