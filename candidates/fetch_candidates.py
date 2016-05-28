#!/usr/bin/python

import logging
from candidates_parser import CandidatesParser
import argparse
import csv

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

arg_parser = argparse.ArgumentParser(description="Fetch candidates by zip codes.")
arg_parser.add_argument('-f', metavar='file', dest='input_file',
                        required=True, help='Input file.')
args = arg_parser.parse_args()

candidateParser = CandidatesParser()

with open(args.input_file) as in_file:
    zip_reader = csv.reader(in_file)
    zip_reader.next()
    for row in zip_reader:
        zip_code = row[0]
        state = row[3]
        if zip_code and state:
            candidateParser.parse_zip(state, zip_code)
