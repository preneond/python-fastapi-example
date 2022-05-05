from typing import Optional

from starlette.requests import Request

from src.core.database import DatabaseConnection


async def get_accept_request_header(request: Request) -> Optional[str]:
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
