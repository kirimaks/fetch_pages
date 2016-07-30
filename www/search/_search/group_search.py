import db_tools
import json


class GroupSearch(object):
    def __init__(self):
        self.db, self.cursor = db_tools.mysql_connect()

    def __del__(self):
        self.db.close()

    def search(self, pattern):
        """ Takes pattern, returns json """

        # Get list of ids.

        # Bad code, need to use Sphinx instead.
        query = """
            SELECT id, first_name, last_name, MATCH(first_name, last_name)
                    AGAINST(%s in natural language mode) as rl
                FROM office_holders
            WHERE MATCH(first_name, last_name)
                AGAINST(%s in natural language mode) > 0
            LIMIT 100
        """

        self.cursor.execute(query, (pattern, pattern))
        id_list = [row[0] for row in self.cursor.fetchall()]

        query = """
            SELECT orgs.org_name, sum(dto.weight)
                FROM doc_to_org_ref AS dto
                    JOIN orgs ON dto.org_id = orgs.org_id
                    JOIN search_space ON dto.doc_id = search_space.rid
                WHERE search_space.candidate_id IN (%s)
            GROUP BY orgs.org_name
            ORDER BY 2 DESC
        """

        # Make string from id list (for IN condition).
        id_list_str = str.join(",", [str(x) for x in id_list])

        self.cursor.execute(query, (id_list_str,))

        results = list()

        for row in self.cursor.fetchall():
            results.append(dict(text=row[0], weight=int(row[1])))

        # Return json.
        return json.dumps(results)


if __name__ == "__main__":
    from pprint import pprint
    gs = GroupSearch()
    pprint(gs.search("william"))
    pprint(gs.search("tom"))
    pprint(gs.search("susan"))
