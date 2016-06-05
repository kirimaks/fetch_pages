import MySQLdb
import timeit


class OrgsSearch(object):
    def connect_db(self):
        mysql = dict(host="localhost", db="parsed_data",
                     user="root", passwd="1234")
        sphinx = dict(host="127.0.0.1", port=9306)
        sp = MySQLdb.connect(**sphinx)
        db = MySQLdb.connect(**mysql)
        return sp, db

    def __del__(self):
        # self.db.close()
        pass

    def __init__(self):
        self.sp, self.db = self.connect_db()
        self.sp_cursor = self.sp.cursor()
        self.db_cursor = self.db.cursor()

    def search(self, search_id):
        query = """
            select org_name from orgs
        """

        sp_query = """
            SELECT count(*)
                FROM parsed_data
                WHERE search_id = 55 AND match(%s)
        """

        self.db_cursor.execute(query)

        results = dict()

        for cur_org in self.db_cursor.fetchall():
            cur_org = cur_org[0]
            cur_org = cur_org.replace('(', '').replace(')', '')  # TODO:
            cur_org = cur_org.replace('/', '\/')
            cur_org = cur_org.replace('!', '\!')

            self.sp_cursor.execute(sp_query, (cur_org,))
            row = self.sp_cursor.fetchone()

            if row:
                results[cur_org] = row[0]

        print(len(results))

if __name__ == "__main__":
    start_time = timeit.default_timer()

    org_searcher = OrgsSearch()
    org_searcher.search(50)

    print(timeit.default_timer() - start_time)
