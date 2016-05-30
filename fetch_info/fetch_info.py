#!/usr/bin/env python

import MySQLdb
import subprocess
import argparse

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-c", metavar="n", dest="count",
                        type=int, help="Requests limit.")
args = arg_parser.parse_args()


class FetchInfo(object):
    def __init__(self, count_limit=None):
        self.count_limit = count_limit
        self.rq_count = 0

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
        name = out[0].replace(' ', '+')
        surname = out[1].replace(' ', '+')
        state = out[2].replace(' ', '+')
        subprocess.call(("/bin/bash", "../scripts/search.sh", name, surname, state))

    def load_id_list(self):
        self.cursor.execute("SELECT id FROM office_holders")

        for some_id in self.cursor.fetchall():
            some_id = some_id[0]
            self.fetch_by_id(some_id)

            if self.count_limit:
                if self.check_count_limit():
                    break

    def check_count_limit(self):
        self.rq_count += 1
        if self.rq_count >= self.count_limit:
            print("Exist due to requests limit.")
            return True     # Exit

fetcher = FetchInfo(args.count)
fetcher.load_id_list()
