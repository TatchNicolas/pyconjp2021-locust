import os
from typing import Optional

from fastapi import Cookie, FastAPI, status
from pydantic import BaseModel
from pymongo import MongoClient
from starlette.responses import Response
from starlette.status import HTTP_400_BAD_REQUEST

APP_MONGO_URL = os.environ["APP_MONGO_URL"]

db = MongoClient(APP_MONGO_URL).get_default_database()
user_col = db["users"]

class User(BaseModel):
    name: str
    password: str

app = FastAPI()

@app.get("/")
def top(name: Optional[str] = Cookie(None)):
    return {"name": name}

@app.post("/users")
def sign_up(user: User, resp: Response):
    resp.status_code = status.HTTP_201_CREATED if user_col.insert_one(user.dict()) else HTTP_400_BAD_REQUEST

@app.post("/auth")
def auth(user: User, resp: Response):
    if user_col.find_one(user.dict()):
        resp.status_code = status.HTTP_200_OK
        resp.set_cookie(key="name", value=user.name)
    else:
        resp.status_code=  status.HTTP_403_FORBIDDEN
