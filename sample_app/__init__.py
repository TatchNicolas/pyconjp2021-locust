from fastapi import FastAPI

from sample_app.models import Login

app = FastAPI()

@app.get("/")
def get_user():
    return "Hi"


@app.post("/users")
def get_user():
    return "Hi"


@app.post("/login")
def get_user(login: Login):
    print(login)
    return "Hi"
