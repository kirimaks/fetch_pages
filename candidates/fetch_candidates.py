#!/usr/bin/python

import logging
import tools
from candidates_parser import CandidatesParser
import argparse

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

argparser = argparse.ArgumentParser(description='Fetch candidates by state, city.')
argparser.add_argument('state', help='State short name (Ex: "NC" or "HI")')
argparser.add_argument('city', help='City name (Ex: "New York")')

args = argparser.parse_args()

state = args.state
city = args.city

zip_codes_list = tools.get_list_of_zip_codes(state, city)

assert zip_codes_list, "empty list (check arguments)"

parser = CandidatesParser(state, city)
for zip_code in zip_codes_list:
    logging.debug("***Processing zip_code ({})***".format(zip_code))
    parser.parse_zip(zip_code)  # And save to db.
