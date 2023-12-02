from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    surname: str
    email: str

user1 = User(id=1, name='pavlos', surname='andreou', email='pavlos@email.com')

@app.get("/")
def index():
    return user1
