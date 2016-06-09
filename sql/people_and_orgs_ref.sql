CREATE TABLE people_and_orgs_ref(
    ref_id      INTEGER PRIMARY KEY AUTO_INCREMENT,
    person_id   INTEGER NOT NULL,
    org_id      INTEGER NOT NULL,
    relevance   INTEGER NOT NULL,
    CONSTRAINT pers_org_rel_uc_ref UNIQUE(person_id, org_id, relevance)
);
