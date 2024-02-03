from datetime import datetime
from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    id: int
    email: EmailStr = Field(...)
    username: str
    password: str
    firstname: str
    lastname: str
    birth_date: datetime
    student_id: int
    profile_picture: str
    createdon: datetime
    role: str
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