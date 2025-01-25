Create database 'users';
USE users;
CREATE TABLE login(username VARCHAR(50) PRIMARY KEY, password VARCHAR(50) );
CREATE USER 'sceta'@'localhost';
GRANT ALL PRIVILEGES ON *.* TO 'sceta'@'localhost';
