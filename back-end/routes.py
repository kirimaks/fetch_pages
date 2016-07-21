from flask import Flask, Response
from flask import render_template
from flask import request
from flask import redirect
import urlparse

from search.people_search import PeopleSearch
from search.group_search import GroupSearch
from search.tweets import search_users

app = Flask(__name__)


# Twitter test
import oauth2

CONS_KEY = "KLgeXShNvyawbCF68xIQnxQ7I"
CONS_SECRET = "m9tqmRVGV2kMSa2Fp6ges4QpTd4cauhXlIi1sb19OclUO2OYpv"

consumer = oauth2.Consumer(CONS_KEY, CONS_SECRET)
client = oauth2.Client(consumer)
request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'
authenticate_url = 'https://api.twitter.com/oauth/authenticate?oauth_token={}'
# /Twitter


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
    # Getting query parameters.
    name = request.args.get("name")

    # Get username or display log in button.
    user_name = request.cookies.get("user_name")

    # Search in twitter api.
    users = search_users(name)
    return render_template("tweets.html", users=users, user_name=user_name)


@app.route("/login")
def login():
    resp, content = client.request(request_token_url, "GET")

    if resp['status'] != '200':
        return "No token", 500

    data = dict(urlparse.parse_qsl(content))

    if data['oauth_callback_confirmed'] == 'true':
        oauth_token = data['oauth_token']
        oauth_token_secret = data['oauth_token_secret']
        resp = redirect(authenticate_url.format(oauth_token))
        resp.set_cookie('oauth_token', oauth_token)
        resp.set_cookie('oauth_token_secret', oauth_token_secret)
        return resp     # Redirect

    return "Login error", 500


@app.route('/auth_req')
def auth_req():
    oauth_token = request.cookies.get('oauth_token')
    oauth_token_secret = request.cookies.get('oauth_token_secret')
    oauth_verifier = request.args.get("oauth_verifier")

    token = oauth2.Token(oauth_token, oauth_token_secret)
    token.set_verifier(oauth_verifier)
    client = oauth2.Client(consumer, token)

    resp, content = client.request(access_token_url, "GET")
    if resp['status'] != '200':
        return "Bad Auth", 500

    data = dict(urlparse.parse_qsl(content))

    # Save user data.
    user_name = data["screen_name"]
    oauth_token = data["oauth_token"]
    oauth_token_secret = data["oauth_token_secret"]

    resp = redirect("/tweets")
    resp.set_cookie("user_name", user_name)
    resp.set_cookie("oauth_token", oauth_token)
    resp.set_cookie("oauth_token_secret", oauth_token_secret)
    return resp


@app.route("/logout")
def logout():
    resp = redirect("/tweets")
    resp.set_cookie("user_name", "", expires=0)
    return resp

if __name__ == "__main__":
    app.run(debug=True)
