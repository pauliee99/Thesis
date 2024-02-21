# Thessis

Command user to start MySQL server:
```
docker run --name mysqldb -v mysqldbvol:/var/lib/mysql -p 3306:3306 -e MYSQL_USER=user -e MYSQL_PASSWORD=password -e MYSQL_DATABASE=events -e MYSQL_ROOT_PASSWORD=password --rm -d mysql/mysql-server:latest
```

Alternatively use: ```docker compose up -d```
delete volumes: ```docker-compose down -v ```

* To connect as root:
```mysql -u root -p```
* To connect as user:
```mysql -h 127.0.0.1 -u user -p```

* Create users:
```
CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON * . * TO 'user'@'localhost';
CREATE USER 'user'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON * . * TO 'user'@'%';
CREATE USER 'user'@'172.17.0.1' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'user'@'172.17.0.1' WITH GRANT OPTION;
```

JSON format to create a new event:
```
{
"displayname": "event1",
"end_time": null,
"id": 1,
"start_time": "2024-01-28T16:39:49",
"picture": "path to file",
"createdon": "2024-01-28T16:39:49",
"location": "kallithea",
"price": 12,
"description": "coolevent",
"createdby": "user1"
}
```


Run fastapi app: `python -m uvicorn main:app --reload`
Run vuejs app: `npm run dev`