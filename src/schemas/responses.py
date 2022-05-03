from typing import List

from pydantic import BaseModel

from schemas.models import User


class ServiceBaseResponse(BaseModel):
    """Response model that is sent when Image Evaluation is requested"""

    success: bool


class UserListResponse(ServiceBaseResponse):
    data: List[User]


class UserResponse(ServiceBaseResponse):
    data: User
