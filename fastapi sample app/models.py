from datetime import datetime
from pydantic import BaseModel

class Student(BaseModel):
    id: int
    email: str
    username: str
    password: str
    firstname: str
    lastname: str
    student_id: int
    profile_picture: str
    createdon: datetime
    disabled: bool

class Manager(BaseModel):
    id: int
    email: str
    username: str
    password: str
    firstname: str
    lastname: str
    profile_picture: str
    createdon: datetime
    disabled: bool

class Admin(BaseModel):
    id: int
    email: str
    username: str
    password: str
    firstname: str
    lastname: str
    profile_picture: str
    createdon: datetime
    disabled: bool

class Event(BaseModel):
    id: int
    displayname: str
    location: str
    start_time: datetime
    end_time: datetime
    price: float
    picture: str
    description: str
    createdon: datetime
    createdby: str