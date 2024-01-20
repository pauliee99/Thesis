CREATE TABLE IF NOT EXISTS events.users(
    id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    email varchar(320),
    username varchar(50),
    password varchar(50),
    firstname varchar(50),
    lastname varchar(50),
    birth_date datetime,
    student_id int,
    profile_picture varchar(256),
    createdon datetime,
    role varchar(50),
    disabled BOOLEAN
);

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
);

CREATE TABLE IF NOT EXISTS events.roles(
    id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    role varchar(50)
);