from fastapi import APIRouter, Depends, Query
from pydantic import EmailStr
from starlette import status
from starlette.responses import JSONResponse

import schemas
from core.database import DatabaseConnection
from core.dependencies import get_db_connection
from core.responses import error_response, success_response

router = APIRouter()


@router.get("/users", response_model=schemas.UserListResponse)
async def get_users(
    db_connection: DatabaseConnection = Depends(get_db_connection),
) -> JSONResponse:
    """
    Returns a list of all users.
    :param db_connection: DatabaseConnection object
    :return: list of all users
    """
    users = db_connection.query_all("SELECT * FROM users")
    return success_response(users)


@router.get("/user", response_model=schemas.UserResponse)
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


@router.post("/user", response_model=schemas.ServiceBaseResponse)
async def create_user_associated_value(
    user_in: schemas.UserCreateRequest,
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


@router.delete("/user", response_model=schemas.ServiceBaseResponse)
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
