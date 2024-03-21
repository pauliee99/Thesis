# select the volum to operate on
FROM mysql/mysql-server:latest

# set the root password
ENV MYSQL_ROOT_PASSWORD=password

# copy sql files inside the docker image
COPY ./sql-init/db_create_users.sql /docker-entrypoint-initdb.d/
COPY ./sql-init/db_create_tables.sql /docker-entrypoint-initdb.d/
COPY ./sql-init/db_add_sample_users.sql /docker-entrypoint-initdb.d/

# run MySQL commands to execute the SQL script
# RUN service mysql start && mysql -u root -p${MYSQL_ROOT_PASSWORD} < /docker-entrypoint-initdb.d/db_create_users.sql
# RUN service mysql start && mysql -u root -p${MYSQL_ROOT_PASSWORD} < /docker-entrypoint-initdb.d/db_create_tables.sql
# RUN service mysql start && mysql -u root -p${MYSQL_ROOT_PASSWORD} < /docker-entrypoint-initdb.d/db_add_sample_users.sql

# expose the MySQL port
EXPOSE 3306