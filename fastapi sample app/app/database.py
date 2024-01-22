from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Session, select

class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    username: str
    password: str
    firstname: str
    lastname: str
    birth_Date: datetime
    student_id: Optional[int] = None
    profile_picture: str
    createdon: datetime
    role: int
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

# Add dummy data
user_1 = Users(
    email="user1@mail.com",
    username="user1",
    password="fakehashedpassword",
    firstname="john",
    lastname="wick",
    birth_Date=datetime.strptime("21/12/1999", "%d/%m/%Y"),
    student_id=None,
    profile_picture="path/to/file",
    createdon=datetime.strptime("21/01/2024", "%d/%m/%Y"),
    role=3,
    disabled=False
)

engine = create_engine("mysql+mysqlconnector://user:password@localhost/events")

SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    session.add(user_1)
    session.commit()

def insert_event(event):
    with Session(engine) as session:
        event_instance = Events(**event)
        session.add(event_instance)
        session.commit()
    
def get_all_events():
    with Session(engine) as session:
        events = session.query(Events).all()
        return events

def get_event_by_id(event_id):
    with Session(engine) as session:
        statement = select(Events).where(Event.id == event_id)
        events = session.exec(statement)
        return events.fetchall()

def delete_event_by_id(event_id):
    with Session(engine) as session:
        event = session.get(Events, event_id)
        session.delete(event)
        session.commit()
    msg = {"message": f"Event with ID {event_id} deleted successfully"}
    return msg
    
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
        statement = select(Users)
        results = session.exec(statement)
        return results.fetchall()