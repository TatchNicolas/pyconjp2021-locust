from typing import Optional

from fastapi import Cookie, FastAPI, status
from pydantic import BaseModel
from starlette.responses import Response

from sample.config import APP_MONGO_USER_COL
from sample.database import db

user_col = db[APP_MONGO_USER_COL]


class User(BaseModel):
    name: str
    password: str


app = FastAPI()


@app.get("/")
def top(resp: Response, name: Optional[str] = Cookie(None)):
    if name:
        return {"name": name}
    resp.status_code = status.HTTP_403_FORBIDDEN
    return {"message": "please login via /auth"}


@app.post("/auth")
def auth(user: User, resp: Response):
    if user_col.find_one(user.dict()):
        resp.status_code = status.HTTP_200_OK
        resp.set_cookie(key="name", value=user.name)
    else:
        resp.status_code = status.HTTP_403_FORBIDDEN
