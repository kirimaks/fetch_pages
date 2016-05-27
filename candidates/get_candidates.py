import bs4
import requests
import logging
import MySQLdb

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


api_key = 'e1819095ba39161837e6b61942b34ba5'
zip_code = '20902'

zip_url = "http://api.votesmart.org/Officials.getByZip?\
                        key={api_key}&zip5={zip_code}"


class CandidateParser(object):
    def __init__(self, url):
        resp = requests.get(url)
        self.parsed_doc = bs4.BeautifulSoup(resp.text, "xml")
        assert resp.status_code == 200, 'Response return not 200'

        logging.debug("Open MySQL")
        self.db = MySQLdb.connect('localhost', 'root', '1234', 'parsed_data')
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()

    def parse_candidates_by_zip(self, zip_code):
        """ Parse candidates by zip code and store to database. """

        for candidate in self.parsed_doc.find_all('candidate'):
            candidate_id = candidate.find('candidateId').get_text()
            log.debug("Processing for candidate: [{}]".format(candidate_id))
            first_name = candidate.find('firstName').get_text()
            last_name = candidate.find('lastName').get_text()

            log.debug("{:10}first_name: {}".format('', first_name))
            log.debug("{:10}last_name: {}".format('', last_name))

            assert first_name, "Frist name is empty"
            assert last_name, "Last name is empty"

            self.save_candidate(first_name, last_name, zip_code)

    def save_candidate(self, first_name, last_name, zip_code):
        query = """INSERT INTO office_holders(first_name, last_name, zip_code)
                        VALUES(%s, %s, %s)"""

        try:
            self.cursor.execute(query, (first_name, last_name, zip_code))
            self.db.commit()
        except:
            self.db.rollback()

url = zip_url.format(api_key=api_key, zip_code=zip_code)
candidate = CandidateParser(url)
candidate.parse_candidates_by_zip(zip_code)
