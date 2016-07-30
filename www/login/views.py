from login import login_app
from flask import redirect, request
import oauth2
from main import config
import os
import urlparse

conf_name = os.environ.get("FLASK_CONFIG", "default")

CONS_KEY = config[conf_name].CONS_KEY
CONS_SECRET = config[conf_name].CONS_SECRET

consumer = oauth2.Consumer(CONS_KEY, CONS_SECRET)
client = oauth2.Client(consumer)
request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'
authenticate_url = 'https://api.twitter.com/oauth/authenticate?oauth_token={}'
#


@login_app.route("/login")
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


@login_app.route('/auth_req')
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


@login_app.route("/logout")
def logout():
    resp = redirect("/tweets")
    resp.set_cookie("user_name", "", expires=0)
    return resp
