#!/usr/bin/env python

import MySQLdb
import subprocess
import argparse
import time
from MySQLdb import OperationalError

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-c", metavar="n", dest="count",
                        type=int, help="Requests limit.")
arg_parser.add_argument("-s", metavar="n", dest="start_limit",
                        type=int, help="Start from n line in search database",
                        default=0)
args = arg_parser.parse_args()


class FetchInfo(object):
    def __init__(self, count_limit=None, start_limit=0):
        self.connect_db()
        self.count_limit = count_limit
        self.rq_count = 0
        self.delay_time = 3
        self.start_limit = start_limit

    def connect_db(self):
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

        try:
            self.cursor.execute(query)

        except OperationalError:    # Reconnect.
            time.sleep(5)
            self.connect_db()
            self.cursor.execute(query)

        out = self.cursor.fetchall()[0]
        name = out[0].replace(' ', '+')
        surname = out[1].replace(' ', '+')
        state = out[2].replace(' ', '+')

        subprocess.call(("/bin/bash", "../scripts/search.sh",
                         name, surname, state, str(candidate_id)))

    def load_id_list(self):

        self.cursor.execute("""SELECT id
                FROM office_holders
                LIMIT {}, 18446744073709551615""".format(self.start_limit))

        for some_id in self.cursor.fetchall():
            some_id = some_id[0]
            self.fetch_by_id(some_id)

            if self.count_limit:
                if self.check_count_limit():
                    break

            print("Waiting: [{}] seconds...".format(self.delay_time))
            time.sleep(self.delay_time)

    def check_count_limit(self):
        self.rq_count += 1
        if self.rq_count >= self.count_limit:
            print("Exit due to requests limit.")
            return True     # Exit

fetcher = FetchInfo(args.count, args.start_limit)
fetcher.load_id_list()
