from typing import Any, Dict

from fastapi import APIRouter
from starlette.requests import Request

from src.utils.responses import success_response

router = APIRouter()


@router.get("/users")
async def get_users(request: Request) -> Dict[str, Any]:
    """
    Returns a list of all users.
    :param request: request object
    :return: list of all users
    """
    return success_response({"users": ["user1", "user2"]})


@router.get("/user/{email}")
async def get_user_associated_value(email: str, request: Request) -> Dict[str, Any]:
    """
    Returns the plain text value associated with the provided email address.
    :param email: user's email address
    :param request: request object
    :return: plain text value associated with the provided email address
    """
    return success_response({"value": "value"})


@router.post("/user/{email}")
async def create_user_associated_value(email: str, request: Request) -> Dict[str, Any]:
    """
    Creates the plain text value associated with the provided email address.
    :param email: user's email address
    :param request: request object
    :return: plain text value associated with the provided email address
    """
    return success_response()


@router.delete("/user/{email}")
async def delete_user_associated_value(email: str, request: Request) -> Dict[str, Any]:
    """
    Deletes plain text value associated with the provided email address.
    :param email: user's email address
    :param request: request object
    :return: plain text value associated with the provided email address
    """
    return success_response()
