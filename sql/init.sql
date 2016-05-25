DROP DATABASE IF exists parsed_data;
CREATE DATABASE parsed_data;
USE parsed_data;

CREATE TABLE search(
    search_id       INTEGER PRIMARY KEY AUTO_INCREMENT,
    search_string   VARCHAR(767) NOT NULL
)ENGINE=INNODB;

CREATE TABLE search_space(
    rid         INTEGER PRIMARY KEY AUTO_INCREMENT,     -- row id
    search_id   INTEGER NOT NULL,
    content     VARCHAR(60000),
    url         VARCHAR(1000) NOT NULL,
    FOREIGN KEY (search_id) REFERENCES search(search_id) ON DELETE CASCADE
)ENGINE=INNODB;
