import MySQLdb


class PeopleSearch(object):
    def mysql_connect(self):
        client = dict(host="localhost", db="parsed_data",
                      user="root", passwd="1234")
        conn = MySQLdb.connect(**client)
        return conn

    def sphinx_connect(self):
        client = dict(host="127.0.0.1", port=9306)
        conn = MySQLdb.connect(**client)
        return conn

    def __init__(self):
        self.sp = self.sphinx_connect()
        self.sp_cursor = self.sp.cursor()

        self.db = self.mysql_connect()
        self.db_cursor = self.db.cursor()

    def __del__(self):
        self.sp.close()

    def search(self, org_name):

        # Check if the organisation exists.
        # If not, return empty list.
        mysql_query = """
            SELECT org_id
                FROM orgs
                WHERE org_name = %s LIMIT 1;
        """

        self.db_cursor.execute(mysql_query, (org_name,))
        buff = self.db_cursor.fetchone()
        if not buff:
            return []

        sphinx_query = """
            SELECT candidate_id, count(*)
                FROM parsed_data WHERE match(%s)
            GROUP BY candidate_id;
        """

        mysql_query = """
            SELECT first_name, last_name
                FROM office_holders
                WHERE id = %s LIMIT 1
        """

        self.sp_cursor.execute(sphinx_query, (org_name,))

        results = list()
        for row in self.sp_cursor.fetchall():
            candidate_id = row[0]
            candidate_weight = row[1]

            self.db_cursor.execute(mysql_query, (candidate_id,))
            buff = self.db_cursor.fetchone()

            cur_candidate = dict(text=u"{} {}".format(buff[0], buff[1]),
                                 weight=candidate_weight)

            results.append(cur_candidate)

        return results


if __name__ == "__main__":
    from pprint import pprint
    people_searcher = PeopleSearch()
    out = people_searcher.search('National Journal')
    pprint(out)
    out = people_searcher.search('Vote Hemp')
    pprint(out)
    out = people_searcher.search('Right March')
    pprint(out)
