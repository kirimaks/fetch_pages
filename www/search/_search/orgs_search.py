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
            SELECT orgs.org_name, dto.weight
                FROM doc_to_org_ref AS dto
                    JOIN orgs ON dto.org_id = orgs.org_id
                    JOIN search_space ON dto.doc_id = search_space.rid
                WHERE search_space.candidate_id = %s
            GROUP BY orgs.org_name
            ORDER BY 2 DESC
        """

        self.db_cursor.execute(query, (candidate_id,))

        results = list()

        for buff in self.db_cursor.fetchall():
            results.append(dict(text=buff[0], weight=buff[1]))

        return results

if __name__ == "__main__":
    org_searcher = OrgsSearch()
    out = org_searcher.search(478)
    print(out)
