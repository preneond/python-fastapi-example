from typing import List

from pydantic import BaseModel

from src.schemas.models import User


class ServiceBaseResponse(BaseModel):
    success: bool


class UserListResponse(ServiceBaseResponse):
    data: List[User]


class UserResponse(ServiceBaseResponse):
    data: User
