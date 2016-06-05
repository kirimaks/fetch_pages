import logging
import bs4
import requests
from candidates_backend import CandidatesBackend

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class CandidatesParser(object):
    def __init__(self):
        self.api_key = 'e1819095ba39161837e6b61942b34ba5'
        self.backend = CandidatesBackend()
        self.official_zip_url = "http://api.votesmart.org/Officials.getByZip?\
                        key={api_key}&zip5={zip_code}"
        self.candidate_zip_url = "http://api.votesmart.org/Candidates.getByZip?\
                        key={api_key}&zip5={zip_code}"

    def parse_zip(self, state, zip_code, category):
        zip_code_id = self.backend.get_zip_code(zip_code, state)

        if category == "officials":
            url = self.official_zip_url.format(api_key=self.api_key,
                                               zip_code=zip_code)
        elif category == "candidates":
            url = self.candidate_zip_url.format(api_key=self.api_key,
                                                zip_code=zip_code)

        resp = requests.get(url)
        assert resp.status_code == 200, 'api.votesmart.org return not 200'
        self.parsed_doc = bs4.BeautifulSoup(resp.text, "xml")

        for candidate in self.parsed_doc.find_all('candidate'):
            candidate_id = candidate.find('candidateId').get_text()
            log.debug("Processing for candidate: [{}]".format(candidate_id))
            first_name = candidate.find('firstName').get_text()
            last_name = candidate.find('lastName').get_text()

            self.backend.save_candidate(candidate_id, first_name,
                                        last_name, zip_code_id)
