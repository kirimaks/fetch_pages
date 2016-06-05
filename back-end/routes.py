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


@app.route("/search/<int:search_id>")
def search_by_id(search_id):
    org_searcher = OrgsSearch()
    results = org_searcher.search(search_id)

    resp = Response(response=json.dumps(results),
                    status=200,
                    mimetype="application/json")
    return resp


@app.route("/get_id/<name>")
def get_id(name):
    name = name.split(" ")

    if not name[0] or not name[1]:
        return "0"

    conn = mysql.connect()
    cursor = conn.cursor()

    query = """
        SELECT search_id
        FROM search
            WHERE search_string LIKE '%{name}+{surname}%' LIMIT 1
    """

    cursor.execute(query.format(name=name[0], surname=name[1]))
    user_id = cursor.fetchone()

    if user_id:
        return str(user_id[0])
    else:
        return "0"


if __name__ == "__main__":
    app.run()
