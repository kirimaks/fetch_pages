--  ----- CLEAN -----------------------------
DROP TABLE IF EXISTS office_holders;
DROP TABLE IF EXISTS zip_codes;
DROP TABLE IF EXISTS states;
--  -----------------------------------------

CREATE TABLE states(
    id      INTEGER PRIMARY KEY AUTO_INCREMENT,
    name    VARCHAR(20) UNIQUE
)ENGINE=INNODB;

CREATE TABLE zip_codes(
    id      INTEGER PRIMARY KEY AUTO_INCREMENT,
    code    INTEGER NOT NULL UNIQUE,
    state   INTEGER NOT NULL REFERENCES states(id)
)ENGINE=InnoDB;

CREATE TABLE office_holders(
    id          INTEGER PRIMARY KEY,                        -- take id from smartvote api
    zip_code_id INTEGER NOT NULL REFERENCES zip_codes(id),
    first_name  VARCHAR(100) NOT NULL, 
    last_name   VARCHAR(100) NOT NUll
)ENGINE=INNODB;

-- ----- VIEWS -------
-- Number of candidates by state.
CREATE VIEW candidates_in_state_view AS
    SELECT states.name AS StateName, count(office_holders.id) AS OfficeHolders
        FROM states JOIN zip_codes ON zip_codes.state = states.id 
            JOIN office_holders ON office_holders.zip_code_id = zip_codes.id  
    GROUP BY states.name;
;

-- Number of candidates by zip_code.
CREATE VIEW candidates_by_zip_code_view AS
    SELECT code AS ZipCode, count(office_holders.id) AS OfficeHolders
        FROM zip_codes JOIN office_holders ON zip_codes.id = office_holders.zip_code_id 
    GROUP BY zip_codes.code
;
