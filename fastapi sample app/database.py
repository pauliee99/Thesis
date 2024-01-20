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
        CREATE TABLE IF NOT EXISTS events.student(
            id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
            email varchar(320),
            username varchar(50),
            password varchar(50),
            firstname varchar(50),
            lastname varchar(50),
            student_id int,
            profile_picture varchar(256),
            createdon datetime,
            disabled BOOLEAN
        )
    """)
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS events.manager(
            id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
            email varchar(320),
            username varchar(50),
            password varchar(50),
            firstname varchar(50),
            lastname varchar(50),
            profile_picture varchar(256),
            createdon datetime,
            disabled BOOLEAN
        )
    """)
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS events.admin(
            id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
            email varchar(320),
            username varchar(50),
            password varchar(50),
            firstname varchar(50),
            lastname varchar(50),
            profile_picture varchar(256),
            createdon datetime,
            disabled BOOLEAN
        )
    """)
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

def delete_event_by_id(event_id):
    try:
        mycursor = mydb.cursor()
        mycursor.execute("delete from events.events where id="+ str(event_id) +";")
        if mycursor.rowcount == 1:
            mydb.commit()
            msg = {"message": f"Event with ID {event_id} deleted successfully"}
        elif mycursor.rowcount > 1:
            mydb.commit()
            msg = {"message": f"Total rows of {str(mycursor.rowcount)} with ID {event_id} deleted successfully"}
        else:
            msg = {"message": f"Event with ID {event_id} not found, no rows affected"}
        mycursor.close()
        mydb.close()
        return msg
    except mysql.connector.Error as err:
        mycursor.close()
        mydb.close()
        return {"error": f"MySQL error: {err}"}
    
def db_info():
    mycursor = mydb.cursor()
    mycursor.execute("SHOW DATABASES;")
    databases = mycursor.fetchall()
    mycursor.execute("SHOW TABLES;")
    tables = mycursor.fetchall()
    mycursor.close()
    db_info = {"databases": databases, "tables": tables}
    return {"Database Iformation": db_info}

def get_all_users():
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("select * from events.admin;")
    users_db = mycursor.fetchall()
    mycursor.close()
    return users_db