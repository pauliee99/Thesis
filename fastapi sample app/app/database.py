from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlmodel import Field, SQLModel, create_engine, Session, select, update
from typing import AsyncGenerator
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker, load_only
from sqlalchemy import join, func
import os

engine = create_engine("mysql+mysqlconnector://user:password@localhost/events")

class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    username: str
    password: str
    firstname: str
    lastname: str
    birth_date: Optional[datetime] = None
    student_id: Optional[int] = None
    profile_picture: str
    createdon: datetime
    role: str
    disabled: bool

class Events(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    displayname: str
    location: str
    start_time: datetime
    end_time: datetime
    price: float
    picture: str
    description: str
    createdon: datetime
    createdby: str

class Roles(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    role: str

class UserEvents(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user: int
    event: int
    timestamp: Optional[float] = Field(default=None)

# Add dummy data
# user_1 = Users(
#     email="user1@mail.com",
#     username="user1",
#     password="fakehashedpassword",
#     firstname="john",
#     lastname="wick",
#     birth_date=datetime.strptime("21/12/1999", "%d/%m/%Y"),
#     student_id=None,
#     profile_picture="path/to/file",
#     createdon=datetime.strptime("21/01/2024", "%d/%m/%Y"),
#     role=3,
#     disabled=False
# )

SQLModel.metadata.create_all(engine)

# with Session(engine) as session:
#     session.add(user_1)
#     session.commit()

def insert_event(event):
    with Session(engine) as session:
        event_instance = Events(**event)
        session.add(event_instance)
        session.commit()
    
def get_all_events():
    with Session(engine) as session:
        events = session.query(Events).all()
        # for event in events:
        #     if os.path.exists(event.picture): 
        #         with open(event.picture, "rb") as image_file:
        #             imgData = image_file.read()
        #         event.picture = imgData
        #     else:
        #         event.picture = None
            
            # event.picture = image_data
    return events

def get_event_by_id(event_id):
    with Session(engine) as session:
        statement = select(Events).where(Events.id == event_id)
        events = session.exec(statement).first()
        return events

def delete_event_by_id(event_id):
    with Session(engine) as session:
        event = session.query(Events).get(event_id)
        if event:
            session.delete(event)
            session.commit()
            return {"message": f"Event with ID {event_id} deleted successfully"}
        else:
            return {"message": f"Event with ID {event_id} not found"}

def update_event(event):
    with Session(engine) as session:
        statement = (
            update(Events)
            .where(Events.id == event.id)
            .values(
                end_time=event.end_time,
                start_time=event.start_time,
                picture=event.picture,
                createdon=event.createdon,
                displayname=event.displayname,
                location=event.location,
                price=event.price,
                description=event.description,
                createdby=event.createdby
            )
        )
        session.exec(statement)
        session.commit()
        return {"message": f"User with ID {event.id} updated successfully"}
    
def db_info():
    with Session(engine) as session:
        # Get a list of databases
        statement_databases = select("Database").distinct()
        databases = session.exec(statement_databases).fetchall()

        # Get a list of tables in the current database
        current_database = engine.url.database
        statement_tables = select("Table").column("Tables_in_" + current_database)
        tables = session.exec(statement_tables).fetchall()

    db_info = {"databases": databases, "tables": tables}
    return {"Database Information": db_info}

def get_all_users():
    with Session(engine) as session:
        users = session.query(Users).join(Roles, Users.role == Roles.id).all()
        # for user in users:
        #     # rolevalue = session.exec(select(Roles.role).where(str(Roles.id) == user.role)).first()
        #     rolevalue = session.scalar(select(Roles.role).where(Roles.id == user.role))
        #     print(rolevalue)
        #     user.role = rolevalue
        return users # at some point i shoule make it return the real role

def insert_user(user):
    with Session(engine) as session:
        user_instance = Users(
            email=user.email,
            username=user.username,
            password=user.password,
            firstname=user.firstname,
            lastname=user.lastname,
            birth_date=user.birth_date,
            student_id=user.student_id,
            profile_picture=user.profile_picture,
            createdon=datetime.now(),
            role=user.role,
            disabled=False
        ) # **user
        session.add(user_instance)
        session.commit()

def get_user_by_email(user_email):
    with Session(engine) as session:
        statement = select(Users.id, Users.username, Users.email, Users.firstname, Users.lastname, Users.student_id, Users.birth_date, Users.profile_picture, Roles.role) \
            .select_from(join(Users, Roles, Users.role == Roles.id)) \
            .where(Users.email == user_email)
        user = session.exec(statement).fetchone()
        user_dict = {
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "firstname": user[3],
            "lastname": user[4],
            "student_id": user[5],
            "birth_date": user[6],
            "profile_picture": user[7],
            "role": user[8]
        }
        return user_dict

def get_user_by_username(username):
    with Session(engine) as session:
        statement = select(Users.id, Users.username, Users.email, Users.firstname, Users.lastname, Users.student_id, Users.birth_date, Users.profile_picture, Roles.role)  \
            .select_from(join(Users, Roles, Users.role == Roles.id)) \
            .where(Users.username == username)
        user = session.exec(statement).fetchone()
        user_dict = {
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "firstname": user[3],
            "lastname": user[4],
            "student_id": user[5],
            "birth_date": user[6],
            "profile_picture": user[7],
            "role": user[8]
        }
        return user_dict

def get_user_by_id(id):
    with Session(engine) as session:
        statement = select(Users.id, Users.username, Users.email, Users.firstname, Users.lastname, Users.student_id, Users.birth_date, Users.profile_picture, Roles.role)  \
            .select_from(join(Users, Roles, Users.role == Roles.id)) \
            .where(Users.id == id)
        user = session.exec(statement).fetchone()
        user_dict = {
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "firstname": user[3],
            "lastname": user[4],
            "student_id": user[5],
            "birth_date": user[6],
            "profile_picture": user[7],
            "role": user[8]
        }
        return user_dict
    
def get_credentials(id):
    with Session(engine) as session:
        statement = select(Users.id,Users.email, Users.password)  \
            .where(Users.id == id)
        user = session.exec(statement).fetchone()
        user_dict = {
            "id": user[0],
            "email": user[1],
            "password": user[2]
        }
        return user_dict

def update_user(user):
    with Session(engine) as session:
        statement = (
            update(Users)
            .where(Users.id == user.id)
            .values(
                email=user.email,
                username=user.username,
                firstname=user.firstname,
                lastname=user.lastname,
                birth_date=user.birth_date,
                student_id=user.student_id,
                profile_picture=user.profile_picture,
                disabled=user.disabled
                # password=user.password,
                # role=user.role,
            )
        )
        session.exec(statement)
        session.commit()
        return {"message": f"User with ID {user.id} updated successfully"}

def update_password(user):
    with Session(engine) as session:
        statement = (
            update(Users)
            .where(Users.id == user.id)
            .values(
                password=user.new_password
            )
        )
        session.exec(statement)
        session.commit()
        return {"message": f"User with ID {user.id} updated successfully"}
    
def get_role(user_email):
    with Session(engine) as session:
        statement = select(Roles).join(Users, Roles.id == Users.role).where(Users.email == user_email)
        role = session.exec(statement)
        return role.first() ## na to allaksa na ferni 1 piso
    
def get_roles():
    with Session(engine) as session:
        return session.query(Roles).all()
    
def insert_role(rolename: str):
    with Session(engine) as session:
        session.add(Roles(
            id = 0,
            role=rolename
        ))
        session.commit()

def get_all_userevents():
    with Session(engine) as session:
        events = session.query(UserEvents).all()
    return events

def get_current_userevents(userid):
    with Session(engine) as session:
        statement = select(UserEvents).where(UserEvents.user == userid)
        users = session.exec(statement).fetchall()
        return users

# def get_event_users(eventid):
#     with Session(engine) as session:
#         statement = select(Users.id, func.concat(Users.firstname, ' ', Users.lastname).label('full_name'), Users.email).join(Users, UserEvents.user == Users.id).where(UserEvents.event == eventid)
#         users = session.exec(statement).fetchall()
#         return users

def get_event_users(eventid):
    with Session(engine) as session:
        statement = (
            select(
                Users.id,
                func.concat(Users.firstname, ' ', Users.lastname).label('full_name'),
                Users.email
            )
            .select_from(UserEvents)
            .join(Users, UserEvents.user == Users.id)
            .where(UserEvents.event == eventid)
        )
        users = session.exec(statement).fetchall()
        users_list = []
        for row in users:
            users_list.append({
                "id": row[0],
                "name": row[1],
                "email": row[2],
            })
        return users_list
    
def insert_user_event(eventuser):
        with Session(engine) as session:
            event_instance = UserEvents(
                user=eventuser.user,
                event=eventuser.event,
                timestamp=datetime.timestamp(datetime.now()),
            )
            session.add(event_instance)
            session.commit()

def delete_user_event(deleteuserevent):
    with Session(engine) as session:
        event = session.query(UserEvents).filter_by(user=deleteuserevent.user, event=deleteuserevent.event).first()
        if event:
            session.delete(event)
            session.commit()
            return {"message": f"Event deleted successfully"}
        else:
            return {"message": f"Event not found"}
        
def get_user_event_record(user_id, event_id):
    with Session(engine) as session:
        statement = (
            select(
                UserEvents
            )
            .select_from(UserEvents)
            .where(UserEvents.event == event_id and UserEvents.user == user_id)
        )
        record = session.exec(statement).fetchall()
        return record