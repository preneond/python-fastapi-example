from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    value: str
