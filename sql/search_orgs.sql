-- search_orgs(search_id, at_least) procedure.
-- "search_id" : id from "search"
-- "at_least"  : int, at least occurences of the tag
-- Takes id from search table and "retuns table" with occurences of organisations.

DROP PROCEDURE if exists search_orgs;

DELIMITER $$

CREATE PROCEDURE search_orgs(search_id INTEGER, at_least INTEGER)
BEGIN

    -- Variables --------------------------------------
    DECLARE orgs_finished   INTEGER DEFAULT 0;
    DECLARE cur_org         VARCHAR(255) DEFAULT '';
    -- ------------------------------------------------

    -- Cursor ------------------------------------
    DECLARE orgs_cursor CURSOR FOR
        SELECT org_name FROM orgs;

    DECLARE CONTINUE HANDLER 
        FOR NOT FOUND SET orgs_finished = 1;
    -- -------------------------------------------

    -- Opening cursor.
    OPEN orgs_cursor;

    -- Results table ----------------------------------
    DROP TEMPORARY TABLE IF EXISTS results;
    CREATE TEMPORARY TABLE results(
        company     VARCHAR(255),
        occurences  INTEGER
    )Engine=Memory;
    -- ------------------------------------------------

    -- Iterate -----------------------------------
    WHILE orgs_finished = 0 DO

        FETCH orgs_cursor INTO cur_org;

        INSERT INTO results(
            SELECT cur_org, count(ss.rid) 
                FROM search_space as ss
                    WHERE ss.search_id = search_id
                        AND MATCH(ss.content) AGAINST(cur_org));

    END WHILE;
    -- -------------------------------------------

    -- Show results ----------------------------------------------
    SELECT * from results WHERE occurences >= at_least ORDER BY 2;
    -- -----------------------------------------------------------

    -- Closing cursor.
    CLOSE orgs_cursor;

END$$

DELIMITER ;
