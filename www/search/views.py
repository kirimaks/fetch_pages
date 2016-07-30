from search import search_app
from flask import render_template, Response
from ._search.group_search import GroupSearch
from ._search.people_search import PeopleSearch


@search_app.route("/")
def hello():
    return render_template("hello.html")


@search_app.route("/group_search/<pattern>")
def group_search(pattern):
    group_searcher = GroupSearch()

    # Takes pattern, returns json.
    results = group_searcher.search(pattern)

    resp = Response(response=results, status=200, mimetype="application/json")
    return resp


@search_app.route("/org_search/<org_name>")
def org_search(org_name):
    people_searcher = PeopleSearch()

    # Takes name, returns json.
    results = people_searcher.search(org_name)

    resp = Response(response=results, status=200, mimetype="application/json")
    return resp
