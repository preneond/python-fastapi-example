import json
from typing import Optional

from fastapi import File, UploadFile
from starlette.requests import Request

from config.annotations import JSONType


async def load_json_file(file: UploadFile = File(...)) -> JSONType:
    """
    Parses a JSON file and returns its content as a JSONObject.
    :param file: input JSON file
    :return: JSONObject with :param file content
    """
    file_data = await file.read()
    json_data = json.loads(file_data)
    return json_data


async def get_accept_request_header(request: Request) -> Optional[str]:
    """
    Returns the value of the Accept header of the request.
    :param request: request
    :return: Accept header value
    """
    return request.headers.get("Accept")
