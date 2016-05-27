--------- CLEAN -----------------------------
DROP TABLE IF EXISTS office_holders;
DROP TABLE IF EXISTS zip_code;
DROP TABLE IF EXISTS state;
---------------------------------------------

CREATE TABLE state(
    id      INTEGER PRIMARY KEY AUTO_INCREMENT,
    name    VARCHAR(100)
)ENGINE=INNODB;

CREATE TABLE zip_code(
    id      INTEGER PRIMARY KEY AUTO_INCREMENT,
    code    INTEGER NOT NULL,
    state   INTEGER NOT NULL REFERENCES state(id)
)ENGINE=InnoDB;

CREATE TABLE office_holders(
    id          INTEGER PRIMARY KEY AUTO_INCREMENT,
    zip_code    INTEGER NOT NULL REFERENCES zip_code(id),
    first_name  VARCHAR(100) NOT NULL, 
    last_name   VARCHAR(100) NOT NUll
)ENGINE=INNODB;

