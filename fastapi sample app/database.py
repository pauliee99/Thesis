# database.py
import mysql.connector
from contextlib import asynccontextmanager

mydb = mysql.connector.connect(
    host="localhost",
    user="user",
    password="password",
    port=3306,
    database="events"
)

def create_event_table():
    mycursor = mydb.cursor()
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS events.events(
            id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
            displayname varchar(128),
            location varchar(256),
            start_time datetime,
            end_time datetime,
            price float,
            picture varchar(256),
            description varchar(512),
            createdon datetime,
            createdby varchar(128)
        )
    """)
    mycursor.close()

def create_user_table():
    mycursor = mydb.cursor()
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS events.users(
            id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
            email varchar(320),
            username varchar(50),
            password varchar(50),
            firstname varchar(50),
            lastname varchar(50),
            student_id int,
            profile_picture varchar(256),
            createdon datetime
        )
    """)
    print("Tables created")
    mycursor.close()

def insert_event(event):
    mycursor = mydb.cursor()
    mycursor.execute("""
        INSERT INTO events.events 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        event.id,
        event.displayname,
        event.location,
        event.start_time,
        event.end_time,
        event.price,
        event.picture,
        event.description,
        event.createdon,
        event.createdby
    ))
    mydb.commit()
    mycursor.close()
    # mycursor.execute(
    #     "insert into events.events values(" + 
    #     str(event.id) + ", '" +
    #     str(event.displayname) + "', '" +
    #     str(event.location) + "', '" +
    #     str(event.start_time) + "', '" +
    #     str(event.end_time) + "', " +
    #     str(event.price) + ", '" +
    #     str(event.picture)   + "', '" +
    #     str(event.description) + "', '" +
    #     str(event.createdon) + "', '" +
    #     str(event.createdby) + "');"
    # )

def get_all_events():
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM events.events;")
    events = mycursor.fetchall()
    mycursor.close()
    return events

def get_event_by_id(event_id):
    mycursor = mydb.cursor()
    mycursor.execute("select * from events.events where id="+ str(event_id) +";")
    event = mycursor.fetchall()
    mycursor.close()
    return event