DROP TABLE IF EXISTS orgs;

CREATE TABLE orgs (
    org_id      INTEGER PRIMARY KEY AUTO_INCREMENT, 
    org_name    VARCHAR(100) NOT NULL,
    full_text   VARCHAR(100)
);
