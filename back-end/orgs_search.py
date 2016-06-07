import MySQLdb


class OrgsSearch(object):
    def connect_db(self):
        mysql = dict(host="localhost", db="parsed_data",
                     user="root", passwd="1234")
        sphinx = dict(host="127.0.0.1", port=9306)
        sp = MySQLdb.connect(**sphinx)
        db = MySQLdb.connect(**mysql)
        return sp, db

    def __del__(self):
        self.db.close()
        self.sp.close()

    def __init__(self):
        self.sp, self.db = self.connect_db()
        self.sp_cursor = self.sp.cursor()
        self.db_cursor = self.db.cursor()

    def search(self, candidate_id):
        query = """
            select org_name from orgs
        """

        sp_query = """
            SELECT count(*)
                FROM parsed_data
                WHERE candidate_id = %s AND match(%s)
        """

        self.db_cursor.execute(query)

        results = list()

        for cur_org in self.db_cursor.fetchall():
            cur_org = cur_org[0]
            cur_org = cur_org.replace('(', '').replace(')', '')  # TODO:
            cur_org = cur_org.replace('/', '\/')
            cur_org = cur_org.replace('!', '\!')

            self.sp_cursor.execute(sp_query, (candidate_id, cur_org))
            occur = self.sp_cursor.fetchone()

            if occur:
                results.append(dict(text=cur_org, weight=occur[0]))

        return results

if __name__ == "__main__":
    org_searcher = OrgsSearch()
    out = org_searcher.search(45)
    print(out)
