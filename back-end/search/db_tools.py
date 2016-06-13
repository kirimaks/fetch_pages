import MySQLdb


def mysql_connect():
    client = dict(user="root", passwd="1234",
                  db="parsed_data")
    db = MySQLdb.connect(**client)
    cursor = db.cursor()
    return db, cursor
