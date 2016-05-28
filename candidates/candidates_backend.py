import MySQLdb
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class CandidatesBackend(object):
    def __init__(self):
        logging.debug("Open MySQL")
        self.db = MySQLdb.connect("localhost", "root", "1234", "parsed_data")
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()

    def get_state_id(self, state):
        query = "SELECT id FROM states WHERE name = '{}'".format(state)
        self.cursor.execute(query)
        state_id = self.cursor.fetchone()

        # Make new state.
        if not state_id:
            logging.debug("Create new state [{}]".format(state))
            query = "INSERT INTO states(name) VALUES('{}')".format(state)
            self.cursor.execute(query)
            self.db.commit()
            self.cursor.execute("SELECT LAST_INSERT_ID()")
            state_id = self.cursor.fetchone()

        return state_id[0]

    def get_zip_code(self, zip_code, state):
        query = """SELECT id FROM zip_codes
                        WHERE code = '{}'""".format(zip_code)
        self.cursor.execute(query)
        zip_code_id = self.cursor.fetchone()

        # Create zip code.
        if not zip_code_id:
            # Get or create state id.
            state_id = self.get_state_id(state)

            logging.debug("Create zip code [{}]".format(zip_code))
            query = """INSERT INTO zip_codes(code, state)
                        VALUES({}, {})""".format(zip_code, state_id)
            self.cursor.execute(query)
            self.db.commit()
            self.cursor.execute("SELECT LAST_INSERT_ID()")
            zip_code_id = self.cursor.fetchone()

        return zip_code_id[0]

    def save_candidate(self, candidate_id, first_name, last_name, zip_code_id):
        query = """INSERT INTO office_holders(id, first_name, last_name, zip_code_id)
                        VALUES(%s, %s, %s, %s)"""
        try:
            self.cursor.execute(query, (candidate_id, first_name,
                                        last_name, zip_code_id))
            self.db.commit()
        except MySQLdb.IntegrityError:
            log.debug("Candidate already exists, skipping...")
            self.db.rollback()
