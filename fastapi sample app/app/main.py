# python -m uvicorn main:app --reload
# http://127.0.0.1:8000/docs

from datetime import datetime, date
from typing import Union
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from enum import Enum
from contextlib import asynccontextmanager
from models.models import User, Event
import models.models
from routers import event_routers, user_routers, userevent_routers
import database
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

events = []
events.append(Event(id=1, displayname="event1", location="kallithea", start_time=datetime.now(), end_time=datetime.now(), price=0.0, picture="picture here", description="a very cool event", createdon = datetime.now(), createdby = "admin"))
events.append(Event(id=2, displayname="event2", location="nea smirni", start_time=datetime.now(), end_time=datetime.now(), price=1.0, picture="picture here", description="another cool event", createdon = datetime.now(), createdby = "admin"))
users = []
users.append(models.models.User(id=1, email="user1@mail.com", username="user1", password="password", firstname="some name", lastname="surname", birth_date=date.today(), student_id=12345, profile_picture="path/to/file", createdon=datetime.now(), role=1, disabled=False))

@asynccontextmanager
async def lifespan(app: FastAPI):
    for event in events:
        database.insert_event(event)
    for user in users:
        database.insert_user(user)
    if len(database.get_roles) == 0:
        roles = ["Student", "Manager", "Admin"]
        for role in roles:
            database.insert_role(role)
    yield

# app = FastAPI(lifespan=lifespan)
app = FastAPI()
#app.add_middleware(HTTPSRedirectMiddleware)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routers.router)
app.include_router(event_routers.router)
app.include_router(userevent_routers.router)

# def hash_password(password: str):
#     return "fakehashed" + password

# class UserInDB(User):
#     password: str

# def decode_token(token):
#     return User(
#         username=token + "fakedecoded", email="john@example.com", firstname="john", lastname="doe"
#     )

# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     user = decode_token(token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user

# @app.post("/token")
# async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
#     users_db = database.get_all_users()
#     formatted_users_db = {user["username"]: user for user in users_db}
#     user_dict = formatted_users_db.get(form_data.username)
#     if not user_dict:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     user = UserInDB(**user_dict)
#     hashed_password = hash_password(form_data.password)
#     if not hashed_password == user.password:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")

#     return {"access_token": user.username, "token_type": "bearer"}

@app.get("/")
async def read_root():
    return {"Hello": "World"}




# @app.get("/users/")
# async def get_all_users(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"token": token}

# @app.get("/users/me")
# async def read_users_me(current_user: Annotated[Student, Depends(get_current_user)]):
#     return current_user 

@app.get("/db_info/")
def test_db():
    return database.db_info()

# @app.on_event("startup")
# async def on_startup():
#     # Not needed if you setup a migration system like Alembic
#     await create_db_and_tables()
