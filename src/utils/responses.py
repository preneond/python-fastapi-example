from typing import Any, Dict, Optional

from fastapi.encoders import jsonable_encoder


def success_response(response_data: Optional[Any] = None) -> Dict[str, Any]:
    if not response_data:
        response_data = {}
    response_json = {"success": True, "data": jsonable_encoder(response_data)}
    return response_json


def error_response(errors: Optional[Any] = None) -> Dict[str, Any]:
    if not errors:
        errors = {}
    response_json = {"success": False, "errors": jsonable_encoder(errors)}
    return response_json
