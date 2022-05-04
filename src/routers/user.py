from fastapi import APIRouter, Depends, Query
from pydantic import EmailStr
from starlette import status
from starlette.responses import JSONResponse

from src.core.database import DatabaseConnection
from src.core.dependencies import get_db_connection
from src.core.responses import error_response, success_response
from src.schemas import requests, responses

router = APIRouter()


@router.get("/users", response_model=responses.UserListResponse)
async def get_users(
    offset: int = Query(default=0),
    limit: int = Query(default=10),
    db_connection: DatabaseConnection = Depends(get_db_connection),
) -> JSONResponse:
    """
    Returns a list of all users.
    :param limit: number of users to return - default 10
    :param offset: offset of the first user to return - default 0
    :param db_connection: DatabaseConnection object
    :return: list of all users
    """
    users = db_connection.query_all(
        "SELECT * FROM users ORDER BY email LIMIT %s OFFSET %s", (limit, offset)
    )
    return success_response(users)


@router.get("/user", response_model=responses.UserResponse)
async def get_user_associated_value(
    email: EmailStr = Query(..., description="Email address of the user"),
    db_connection: DatabaseConnection = Depends(get_db_connection),
) -> JSONResponse:
    """
    Returns the plain text value associated with the provided email address.
    :param email: email address of the user
    :param db_connection: `DatabaseConnection` object
    :return: plain text value associated with the provided email address
    """
    user = db_connection.query_one("SELECT * FROM users WHERE email = %s", (email,))
    if user is not None:
        return success_response(user)
    else:
        return error_response("User not found", status_code=status.HTTP_404_NOT_FOUND)


@router.post("/user", response_model=responses.ServiceBaseResponse)
async def create_user_associated_value(
    user_in: requests.UserCreateRequest,
    email: EmailStr = Query(..., description="Email address of the user"),
    db_connection: DatabaseConnection = Depends(get_db_connection),
) -> JSONResponse:
    """
    Creates the plain text value associated with the provided email address.
    :param email: email address of the user
    :param user_in: `UserCreateRequest` object
    :param db_connection: DatabaseConnection object
    :return: plain text value associated with the provided email address
    """
    db_connection.execute(
        "INSERT INTO users VALUES(%s, %s) ON CONFLICT (email) DO UPDATE SET email = %s;",
        (email, user_in.value, email),
    )
    return success_response()


@router.delete("/user", response_model=responses.ServiceBaseResponse)
async def delete_user_associated_value(
    email: EmailStr = Query(..., description="Email address of the user"),
    db_connection: DatabaseConnection = Depends(get_db_connection),
) -> JSONResponse:
    """
    Deletes plain text value associated with the provided email address.
    :param email: email address of the user
    :param db_connection: DatabaseConnection object
    :return: plain text value associated with the provided email address
    """

    db_connection.execute("DELETE FROM users WHERE email = %s", (email,))

    return success_response()
