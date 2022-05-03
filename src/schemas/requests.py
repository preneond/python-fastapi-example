from pydantic import BaseModel


class UserUpdateRequest(BaseModel):
    value: str


class UserCreateRequest(BaseModel):
    value: str
