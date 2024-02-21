INSERT INTO 
    events.users
VALUES
    (null, "admin@mail.com", "admin", "fakehashedpassword", "name", "surname", "path to file", CURDATE(), false),
    (null, "manager@mail.com", "manager", "fakehashedpassword", "name", "surname", "path to file", CURDATE(), false),
    (null, "student1@mail.com", "student1", "fakehashedpassword", "name", "surname", "path to file", CURDATE(), false);


INSERT INTO 
    events.events
VALUES
    (null, "event1", "kallithea", CURDATE(), CURDATE(), 0, "path to file", "this event is cool", CURDATE(), "admin"),
    (null, "event2", "tavros", CURDATE(), CURDATE(), 5, "path to file", "this event is cool", CURDATE(), "admin"),
    (null, "event3", "monastiraki", CURDATE(), CURDATE(), 5, "path to file", "this event is cool", CURDATE(), "admin");

INSERT INTO 
    events.roles
VALUES
    (null, "Student"),
    (null, "Manager"),
    (null, "Admin");