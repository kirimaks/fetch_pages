DROP TABLE IF EXISTS orgs;

CREATE TABLE orgs (
    org_id      INTEGER PRIMARY KEY AUTO_INCREMENT, 
    org_name    VARCHAR(200) NOT NULL UNIQUE,
    full_text   VARCHAR(10000)
);
