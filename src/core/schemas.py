from typing import List

from pydantic import BaseModel, EmailStr


# db schemas
class User(BaseModel):
    email: EmailStr
    value: str


# response schemas
class ServiceBaseResponse(BaseModel):
    """Response model that is sent when Image Evaluation is requested"""

    success: bool


class UserListResponse(ServiceBaseResponse):
    data: List[User]


class UserResponse(ServiceBaseResponse):
    data: User


# request schemas
class UserCreateRequest(BaseModel):
    value: str


class UserUpdateRequest(BaseModel):
    value: str
