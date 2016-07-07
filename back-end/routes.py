from flask import Flask, Response
from flask import render_template
from flask import request

from search.people_search import PeopleSearch
from search.group_search import GroupSearch
from search.tweets import get_tweets

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("hello.html")


@app.route("/group_search/<pattern>")
def group_search(pattern):
    group_searcher = GroupSearch()

    # Takes pattern, returns json.
    results = group_searcher.search(pattern)

    resp = Response(response=results, status=200, mimetype="application/json")
    return resp


@app.route("/org_search/<org_name>")
def org_search(org_name):
    people_searcher = PeopleSearch()

    # Takes name, returns json.
    results = people_searcher.search(org_name)

    resp = Response(response=results, status=200, mimetype="application/json")
    return resp


@app.route("/tweets")
def tweets():
    tag = request.args.get("tag")
    tweets = get_tweets(tag)
    return render_template("tweets.html", tweets=tweets)


if __name__ == "__main__":
    app.run(debug=True)
