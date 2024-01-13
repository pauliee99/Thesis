# python -m uvicorn main1:app --reload
# http://127.0.0.1:8000/docs

from datetime import datetime
from typing import Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
import mysql.connector
from contextlib import asynccontextmanager
from fastapi.security import OAuth2PasswordBearer

class Student(BaseModel):
    id: int
    fname: str
    lname: str
    username: str
    password: str
    student_id: int
    profile_picture: str
    createdon: datetime

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
    createdon: datetime
    createdby: str

events = []
event2 = Event(id=2, displayname="event2", location="nea smirni", start_time=datetime.now(), end_time=datetime.now(), price=1.0, picture="picture here", description="another cool event", createdon = datetime.now(), createdby = "admin")
events.append(Event(id=1, displayname="event1", location="kallithea", start_time=datetime.now(), end_time=datetime.now(), price=0.0, picture="picture here", description="a very cool event", createdon = datetime.now(), createdby = "admin"))
events.append(event2)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@asynccontextmanager
async def lifespan(app: FastAPI):
    mydb = mysql.connector.connect(
        host="localhost",
        user="user",
        password="password",
        port=3306,
        database="events"
    )
    mycursor = mydb.cursor()
    mycursor.execute("""CREATE TABLE IF NOT EXISTS events.events(
        id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        displayname varchar(128),
        location varchar(256),
        start_time datetime,
        end_time datetime,
        price float,
        picture varchar(256),
        description varchar(512),
        createdon datetime,
        cretedby varchar(128)
    )""")
    mycursor.execute("""CREATE TABLE IF NOT EXISTS events.users(
        id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        username varchar(50),
        password varchar(50),
        firstname varchar(50),
        lastname varchar(50),
        student_id int,
        profile_picture varchar(256),
        createdon datetime
    )""")
    print ("tables created")
    yield
    mycursor.close()
    mydb.close()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/events/")
def get_all_events():
    mydb = mysql.connector.connect(
        host="localhost",
        user="user",
        password="password",
        port=3306,
        database="events"
    )
    mycursor = mydb.cursor()
    mycursor.execute("select * from events.events;")
    events = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    return events

@app.post("/events/")
def create_event(event: Event):
    events.append(event)
    mydb = mysql.connector.connect(
        host="localhost",
        user="user",
        password="password",
        port=3306,
        database="events"
    )
    mycursor = mydb.cursor()
    mycursor.execute(
        "insert into events.events values(" + 
        str(event.id) + ", '" +
        str(event.displayname) + "', '" +
        str(event.location) + "', '" +
        str(event.start_time) + "', '" +
        str(event.end_time) + "', " +
        str(event.price) + ", '" +
        str(event.picture)   + "', '" +
        str(event.description) + "', '" +
        str(event.createdon) + "', '" +
        str(event.createdby) + "');"
    )
    mydb.commit()
    # Close the cursor and connection
    mycursor.close()
    mydb.close()
    return {"message": "Event created successfully", "event": event.dict()}

@app.get("/get_event/{event_id}")
async def get_event(event_id: int):
    mydb = mysql.connector.connect(
        host="localhost",
        user="user",
        password="password",
        port=3306,
        database="events"
    )
    mycursor = mydb.cursor()
    mycursor.execute("select * from events.events where id="+ str(event_id) +";")
    event = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    if len(event) == 0:
        raise HTTPException(status_code=404, detail="Event not found")
    else:
        return event


@app.get("/db_info/")
def test_db():
    mydb = mysql.connector.connect(
        host="localhost",
        user="user",
        password="password",
        port=3306,
        database="events"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SHOW DATABASES;")
    databases = mycursor.fetchall()
    mycursor.execute("SHOW TABLES;")
    tables = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    db_info = {"databases": databases, "tables": tables}
    return {"Database Iformation": db_info}

