from flask import Flask, Response
app = Flask(__name__)

from orgs_search import OrgsSearch
import json


@app.route("/")
def hello():
    return "Hello World!!!"


@app.route("/search/<int:search_id>")
def search_by_id(search_id):
    org_searcher = OrgsSearch()
    results = org_searcher.search(search_id)

    resp = Response(response=json.dumps(results),
                    status=200,
                    mimetype="application/json")
    return resp


if __name__ == "__main__":
    app.run()
