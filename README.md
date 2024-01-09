# Thessis

Command user to start MySQL server:
```
docker run --name mysqldb -v mysqldbvol:/var/lib/mysql -p 3306:3306 -e MYSQL_USER=user -e MYSQL_PASSWORD=password -e MYSQL_DATABASE=events -e MYSQL_ROOT_PASSWORD=password --rm -d mysql/mysql-server:latest
```

To connect as root:
```mysql -u root -p```
