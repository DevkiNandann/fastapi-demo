from lib2to3.pytree import Base
from typing import Optional
from pydantic import BaseModel


class UserBaseModel(BaseModel):
    email: str
    name: str


class SignUp(UserBaseModel):
    password: str


class UsersResponse(UserBaseModel):
    class Config():
        orm_mode = True


class EditUserModel(BaseModel):
    name: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
