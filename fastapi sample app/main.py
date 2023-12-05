from datetime import datetime
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum

class Student(BaseModel):
    id: int
    fname: str
    lname: str
    username: str
    password: str
    student_id: int
    profile_picture: str

class Manager(BaseModel):
    id: int
    fname: str
    lname: str
    username: str
    password: str
    profile_picture: str

class Admin(BaseModel):
    id: int
    fname: str
    lname: str
    username: str
    password: str
    profile_picture: str

class Event(BaseModel):
    id: int
    displayname: str
    location: str
    start_time: datetime
    end_time: datetime
    price: float
    picture: str
    description: str

events = []
event2 = Event(id=2, displayname="event2", location="nea smirni", start_time=datetime.now(), end_time=datetime.now(), price=1.0, picture="picture here", description="another cool event")
events.append(Event(id=1, displayname="event1", location="kallithea", start_time=datetime.now(), end_time=datetime.now(), price=0.0, picture="picture here", description="a very cool event"))
events.append(event2)

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/events/")
def read_item():
    return events
