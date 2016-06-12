DROP TABLE IF EXISTS doc_to_org_ref;

CREATE TABLE doc_to_org_ref(
    ref_id  INTEGER PRIMARY KEY AUTO_INCREMENT,
    doc_id  INTEGER NOT NULL,
    org_id  INTEGER NOT NULL,
    weight  INTEGER NOT NULL,
    CONSTRAINT doc_to_org_uni_ref UNIQUE(doc_id, org_id)
);
