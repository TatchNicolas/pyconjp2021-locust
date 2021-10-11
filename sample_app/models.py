from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    user_id: str
    last_login: datetime


class UserInfo(BaseModel):
    user_id: str
    last_login: datetime


class Login(BaseModel):
    user_id: str
    password: str
