# python -m uvicorn main1:app --reload
# http://127.0.0.1:8000/docs

from datetime import datetime
from typing import Union
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from enum import Enum
import mysql.connector
from contextlib import asynccontextmanager
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

class Student(BaseModel):
    id: int
    email: str
    firstname: str
    lastname: str
    username: str
    password: str
    student_id: int
    profile_picture: str
    createdon: datetime

class Manager(BaseModel):
    id: int
    firstname: str
    lastname: str
    username: str
    password: str
    profile_picture: str

class Admin(BaseModel):
    id: int
    firstname: str
    lastname: str
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
        email varchar(320),
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

def hash_password(password: str):
    return "fakehashed" + password

class UserInDB(Student):
    password: str

def decode_token(token):
    return Student(
        username=token + "fakedecoded", email="john@example.com", firstname="john"
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
    mydb = mysql.connector.connect(
        host="localhost",
        user="user",
        password="password",
        port=3306,
        database="events"
    )
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("select * from events.users;")
    users_db = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    formatted_users_db = {user["username"]: user for user in users_db}
    user_dict = formatted_users_db.get(form_data.username) # [user for user in users_db if user.get("username") == form_data.username]
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

@app.get("/delete_event_by_id/{event_id}")
async def delete_event_by_id(event_id: int):
    mydb = mysql.connector.connect(
        host="localhost",
        user="user",
        password="password",
        port=3306,
        database="events"
    )
    mycursor = mydb.cursor()
    try:
        mycursor.execute("delete from events.events where id="+ str(event_id) +";")
        if mycursor.rowcount == 1:
            mydb.commit()
            msg = {"message": f"Event with ID {event_id} deleted successfully"}
        elif mycursor.rowcount > 1:
            mydb.commit()
            msg = {"message": f"Total rows of " + str(mycursor.rowcount) + " with ID {event_id} deleted successfully"}
        else:
            msg = {"message": f"Event with ID {event_id} not found, no rows affected"}
        mycursor.close()
        mydb.close()
        return msg
    except mysql.connector.Error as err:
        mycursor.close()
        mydb.close()
        return {"error": f"MySQL error: {err}"}

@app.get("/users/")
async def get_all_users(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

@app.get("/users/me")
async def read_users_me(current_user: Annotated[Student, Depends(get_current_user)]):
    return current_user 

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

