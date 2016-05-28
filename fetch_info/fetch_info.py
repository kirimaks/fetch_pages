import MySQLdb
import subprocess


class FetchInfo(object):
    def __init__(self):
        self.db = MySQLdb.connect("localhost", "root", "1234", "parsed_data")
        self.cursor = self.db.cursor()

    def fetch_by_id(self, candidate_id):
        query = """
            SELECT candidate.first_name, candidate.last_name, states.name
                FROM office_holders AS candidate
                    JOIN zip_codes ON zip_codes.id = candidate.zip_code_id
                    JOIN states ON states.id = zip_codes.state
                WHERE candidate.id = {}
        """.format(candidate_id)

        self.cursor.execute(query)
        out = self.cursor.fetchall()[0]
        name = out[0]
        surname = out[1]
        state = out[2]
        subprocess.call(("/bin/bash", "../search.sh", name, surname, state))

    def load_id_list(self):
        self.cursor.execute("SELECT id FROM office_holders")

        for some_id in self.cursor.fetchall():
            some_id = some_id[0]
            self.fetch_by_id(some_id)


fetcher = FetchInfo()
fetcher.load_id_list()
