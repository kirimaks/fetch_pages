#!/usr/bin/python

import logging
from candidates_parser import CandidatesParser
import argparse
import csv
import sys

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

arg_parser = argparse.ArgumentParser(description="""
                        Fetch candidates by zip codes.""")

arg_parser.add_argument('-f', metavar='file', dest='input_file',
                        required=True, help='Zip codes input file.')
arg_parser.add_argument('-c', metavar='category', dest='catg',
                        required=True,
                        help='Set category (officials/candidates)')

args = arg_parser.parse_args()


if args.catg in ('officials', 'candidates'):
    category = args.catg
else:
    print("Unknown category: ({}), exit.".format(args.cat))
    print("Category can be: 'officials', 'candidates'")
    sys.exit(0)


candidateParser = CandidatesParser()

# Reading zip file.
with open(args.input_file) as in_file:
    zip_reader = csv.reader(in_file)
    zip_reader.next()   # Skip header.
    for row in zip_reader:
        zip_code = row[0]
        state = row[2]
        if zip_code and state:
            candidateParser.parse_zip(state, zip_code, category)
