import MySQLdb
import threading


def mysql_connect():
    client = dict(host="localhost", user="root",
                  passwd="1234", db="parsed_data")
    conn = MySQLdb.connect(**client)
    cursor = conn.cursor()
    return conn, cursor


def sphinx_connect():
    client = dict(host="127.0.0.1", port=9306)
    conn = MySQLdb.connect(**client)
    cursor = conn.cursor()
    return conn, cursor


def get_organisations_list(cursor):
    query = """
        SELECT org_id, org_name
            FROM orgs
    """
    cursor.execute(query)
    return {id: name for (id, name) in cursor.fetchall()}


class GroupUpdater(threading.Thread):

    def __init__(self, thread_num):
        threading.Thread.__init__(self)
        self.thread_num = thread_num
        self.conn, self.cursor = mysql_connect()
        self.sphinx_conn, self.sphinx_cursor = sphinx_connect()

    def __del__(self):
        self.conn.close()
        self.sphinx_conn.close()

    def run(self):
        print("*** Thread: {} started ***".format(self.thread_num))

        # Prepare sphinx query.
        search_query = """
            SELECT id as doc_id, weight()
                FROM parsed_data
                WHERE MATCH(%s)
        """

        # Prepare insert query.
        insert_query = """
            INSERT INTO doc_to_org_ref(doc_id, org_id, weight)
                VALUES(%s, %s, %s)
        """

        orgs_list = [i for i in updater.orgs_list.keys() if i % updater.threads_num == self.thread_num]

        for org_id in orgs_list:
            org_name = updater.orgs_list[org_id]
            org_name = org_name.replace('/', r'\/')
            org_name = org_name.replace('\'', r'\'')
            org_name = org_name.replace('!', r'\!')

            self.sphinx_cursor.execute(search_query, (org_name,))

            for buff in self.sphinx_cursor.fetchall():
                doc_id = buff[0]
                weight = buff[1]
                self.cursor.execute(insert_query, (doc_id, org_id, weight))
                self.conn.commit()


class RefUpdater(object):

    def __init__(self):
        self.db, self.cursor = mysql_connect()
        # self.sp, self.sphinx_cursor = sphinx_connect()

        self.orgs_list = get_organisations_list(self.cursor)
        self.threads_num = 4

    def __del__(self):
        self.db.close()
        # self.sp.close()

    def update(self):
        for i in range(self.threads_num):
            thread = GroupUpdater(i)
            thread.start()


updater = RefUpdater()
updater.update()
