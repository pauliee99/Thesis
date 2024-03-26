from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    id: int
    email: EmailStr = Field(...)
    username: str
    password: str
    firstname: str
    lastname: str
    birth_date: date
    student_id: int
    profile_picture: str
    createdon: datetime
    role: int
    disabled: bool

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "joe@xyz.com",
                "password": "any"
            }
        }
    
class Roles(BaseModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    role: str

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
    class Config:
        json_schema_extra = {
            "example": {
                "location": "kallithea",
                "price": 0,
                "description": "this event is cool",
                "createdby": "current user",
                "start_time": "2024-02-04T00:00:00",
                "displayname": "event1",
                "id": 1,
                "end_time": "2024-02-04T00:00:00",
                "picture": "path to file",
                "createdon": "2024-02-04T00:00:00"
            }
        }