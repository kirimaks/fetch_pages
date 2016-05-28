--  ----- CLEAN --------------------------
DROP VIEW IF EXISTS tables_size_view;
DROP TABLE IF EXISTS search_space;
DROP TABLE IF EXISTS search;
--  --------------------------------------

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
CREATE FULLTEXT INDEX content_search ON search_space(content);

CREATE VIEW tables_size_view AS
    SELECT TABLE_NAME AS 'TableName', round(((data_length + index_length) / 1024 / 1024), 2) AS MbSize
    FROM information_schema.TABLES  
    WHERE table_schema = 'parsed_data' ORDER BY MbSize DESC;
;
