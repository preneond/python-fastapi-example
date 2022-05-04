import json

from fastapi import File, UploadFile
from starlette.requests import Request

from src.config.annotations import JSONType
from src.core.database import DatabaseConnection


async def load_json_file(file: UploadFile = File(...)) -> JSONType:
    """
    Parses a JSON file and returns its content as a JSONType.
    :param file: input JSON file
    :return: JSONType with :param file content
    """
    file_data = await file.read()
    json_data = json.loads(file_data)
    return json_data


async def get_accept_request_header(request: Request) -> str | None:
    """
    Returns the value of the Accept header of the request.
    :param request: request
    :return: Accept header value
    """
    return request.headers.get("Accept")


async def get_db_connection(request: Request) -> DatabaseConnection:
    """
    Returns a database connection
    :param request: request
    :return: database connection
    """
    return request.app.state.db_connection
