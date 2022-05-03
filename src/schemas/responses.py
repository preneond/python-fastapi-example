from typing import List

from pydantic import BaseModel

from src import schemas


class ServiceBaseResponse(BaseModel):
    """Response model that is sent when Image Evaluation is requested"""

    success: bool


class UserListResponse(ServiceBaseResponse):
    data: List[schemas.User]


class UserResponse(ServiceBaseResponse):
    data: schemas.User
