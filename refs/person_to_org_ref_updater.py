import MySQLdb


class RefUpdater(object):
    def mysql_connect(self):
        client = dict(host="localhost", user="root",
                      passwd="1234", db="parsed_data")
        conn = MySQLdb.connect(**client)
        cursor = conn.cursor()
        return conn, cursor

    def sphinx_connect(self):
        client = dict(host="localhost", port=9306)
        conn = MySQLdb.connect(**client)
        cursor = conn.cursor()
        return conn, cursor

    def __init__(self):
        self.db, self.cursor = self.mysql_connect()
        self.sp, self.sphinx_cursor = self.mysql_connect()

    def __del__(self):
        self.db.close()
        self.sp.close()

    def update(self):
        query = """
            select * from orgs;
        """

        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            print(row)

        query = """
            show tables;
        """

        self.sphinx_cursor.execute(query)
        for row in self.sphinx_cursor.fetchall():
            print(row)

updater = RefUpdater()
updater.update()
