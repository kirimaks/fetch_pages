import csv
import argparse
import MySQLdb


def get_args():
    arg_parse = argparse.ArgumentParser()
    arg_parse.add_argument("-f", required=True, help="Csv file with organisations.", dest="input_file")
    args = arg_parse.parse_args()
    return args


def db_connect():
    db = MySQLdb.connect("localhost", "root", "1234", "parsed_data")
    return db

args = get_args()

with open(args.input_file) as orgs_list:
    orgs_reader = csv.reader(orgs_list)

    db = db_connect()
    cursor = db.cursor()

    for org_row in orgs_reader:
        org_name = org_row[0].strip()
        query = "INSERT INTO orgs(org_name) VALUES(%s)"
        cursor.execute(query, (org_name,))
        db.commit()

    db.close()
