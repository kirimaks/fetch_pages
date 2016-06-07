from flask import Flask, Response
from flask import render_template
from flask.ext.mysql import MySQL
from orgs_search import OrgsSearch
import json

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_DB'] = 'parsed_data'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route("/")
def hello():
    return render_template("hello.html")


@app.route("/search/<int:candidate_id>")
def search_by_id(candidate_id):
    org_searcher = OrgsSearch()
    results = org_searcher.search(candidate_id)

    resp = Response(response=json.dumps(results),
                    status=200,
                    mimetype="application/json")
    return resp


@app.route("/get_id/<name>")
def get_id(name):

    conn = mysql.connect()
    cursor = conn.cursor()

    query = """
        SELECT *,
            MATCH(first_name, last_name) against(%s  IN BOOLEAN MODE) as rel
            FROM office_holders
                WHERE MATCH(first_name, last_name) against(%s  IN BOOLEAN MODE)
            ORDER BY REL DESC
            LIMIT 1
    """

    cursor.execute(query, (name, name))
    user_id = cursor.fetchone()

    if user_id:
        return str(user_id[0])
    else:
        return "-1"


if __name__ == "__main__":
    app.run()
