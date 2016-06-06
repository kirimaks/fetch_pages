import MySQLdb


class Reindex(object):
    def connect_db(self):
        conn = MySQLdb.connect("localhost", "root", "1234", "parsed_data")
        return conn

    def __init__(self):
        self.db = self.connect_db()
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()

    def indexing(self):
        query = """
            SELECT * FROM search
        """
        self.cursor.execute(query)

        for row in self.cursor.fetchall():
            search_string = row[1]

            buff = search_string.partition('=')[-1]
            buff = buff.split('+')

            first_name = buff[0]
            last_name = buff[1]

            search_id = row[0]

            query = """
                SELECT id
                    FROM office_holders
                    WHERE first_name = %s and last_name = %s
            """

            self.cursor.execute(query, (first_name, last_name))
            candidate_id = self.cursor.fetchone()
            if candidate_id:
                candidate_id = candidate_id[0]

                print(candidate_id, "=>", search_id)

                query = """
                    UPDATE search_space
                        SET candidate_id = %s
                    WHERE search_id = %s
                """
                self.cursor.execute(query, (candidate_id, search_id))
                self.db.commit()

if __name__ == "__main__":
    rx = Reindex()
    rx.indexing()
