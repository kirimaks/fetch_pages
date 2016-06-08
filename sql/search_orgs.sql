DROP PROCEDURE IF EXISTS `search_orgs`;

DELIMITER $$
CREATE PROCEDURE `search_orgs`(candidate_id INTEGER, at_least INTEGER)
BEGIN
    DECLARE orgs_finished   INTEGER DEFAULT 0;
    DECLARE cur_org_name    VARCHAR(255) DEFAULT '';
    DECLARE cur_org_id      INTEGER;
    DECLARE match_buff      INTEGER;
    -- DECLARE output          VARCHAR(65535) DEFAULT '';

    -- Cursor;
    DECLARE orgs_cursor CURSOR FOR
        SELECT org_id, org_name FROM orgs;
    DECLARE CONTINUE HANDLER
        FOR NOT FOUND SET orgs_finished = 1;       

    -- Temporary table;
    CREATE TEMPORARY TABLE results(
        org_id        INTEGER NOT NULL,  
        occurences    INTEGER NOT NULL
    );
    

    OPEN orgs_cursor;

    WHILE orgs_finished = 0 DO
        -- Get an organisation.
        FETCH orgs_cursor INTO cur_org_id, cur_org_name;

        SELECT count(rid)
            FROM search_space
                WHERE candidate_id = candidate_id
                    AND MATCH(content) AGAINST(cur_org_name) LIMIT 1
        INTO match_buff;

        -- Show results.
        IF match_buff > 0 THEN
            -- select cur_org as cur_org, match_buff as matches;
            INSERT INTO results(org_id, occurences)
                VALUES(cur_org_id, match_buff);
        END IF;

    END WHILE;

    CLOSE orgs_cursor;                

    select count(*) from results;

END $$
DELIMITER ; 
