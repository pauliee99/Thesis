# python -m uvicorn main1:app --reload
# http://127.0.0.1:8000/docs

from datetime import datetime
from typing import Union
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from enum import Enum
from contextlib import asynccontextmanager
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.models import User, Event
from routers import event_routers, user_routers
from dependencies import get_token_header, get_query_token
from internal import admin
import database

events = []
event2 = Event(id=2, displayname="event2", location="nea smirni", start_time=datetime.now(), end_time=datetime.now(), price=1.0, picture="picture here", description="another cool event", createdon = datetime.now(), createdby = "admin")
events.append(Event(id=1, displayname="event1", location="kallithea", start_time=datetime.now(), end_time=datetime.now(), price=0.0, picture="picture here", description="a very cool event", createdon = datetime.now(), createdby = "admin"))
events.append(event2)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     yield

# app = FastAPI(lifespan=lifespan)
app = FastAPI()

app.include_router(user_routers.router)
app.include_router(event_routers.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

def hash_password(password: str):
    return "fakehashed" + password

class UserInDB(User):
    password: str

def decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", firstname="john", lastname="doe"
    )

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    users_db = database.get_all_users()
    formatted_users_db = {user["username"]: user for user in users_db}
    user_dict = formatted_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = hash_password(form_data.password)
    if not hashed_password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/events/")
def create_event(event: Event):
    events.append(event)
    database.insert_event(event)
    return {"message": "Event created successfully", "event": event.dict()}

@app.get("/get_event/{event_id}")
async def get_event(event_id: int):
    event = database.get_event_by_id(event_id)
    if len(event) == 0:
        raise HTTPException(status_code=404, detail="Event not found")
    else:
        return event

@app.get("/delete_event_by_id/{event_id}")
async def delete_event_by_id(event_id: int):
    return database.delete_event_by_id(event_id)

# @app.get("/users/")
# async def get_all_users(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"token": token}

# @app.get("/users/me")
# async def read_users_me(current_user: Annotated[Student, Depends(get_current_user)]):
#     return current_user 

@app.get("/db_info/")
def test_db():
    return database.db_info()

