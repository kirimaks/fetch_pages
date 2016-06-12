import csv
import argparse
import MySQLdb
import codecs
from MySQLdb import IntegrityError

# Need to conver csv file to utf8 before using!!!


def get_args():
    arg_parse = argparse.ArgumentParser()
    arg_parse.add_argument("-f", required=True,
                           help="Csv file with organisations.",
                           dest="input_file")
    args = arg_parse.parse_args()
    return args


def db_connect():
    db = MySQLdb.connect("localhost", "root", "1234", "parsed_data")
    return db

args = get_args()


def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')


with codecs.open(args.input_file, encoding="utf8") as orgs_list:
    orgs_reader = csv.reader(utf_8_encoder(orgs_list))

    db = db_connect()
    cursor = db.cursor()

    for org_row in orgs_reader:
        org_name = org_row[0].strip()
        org_name = org_name.decode('utf-8')

        print(u"INSERT: {}, {}".format(org_name, len(org_name)))

        query = u"INSERT INTO orgs(org_name) VALUES(%s)"
        try:
            cursor.execute(query, (org_name,))
            db.commit()
        except IntegrityError:
            print("Skipping dublicate")

    db.close()
