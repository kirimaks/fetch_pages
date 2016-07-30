from tweets import tweets_app
from flask import request, render_template
from .twiter_oauth import get_user_info, search_users
from .twiter_oauth import post_new_tweet
import json


@tweets_app.route("/")
def tweets():
    # Getting query parameters.
    name = request.args.get("name")

    # Get username or display log in button.
    user_name = request.cookies.get("user_name", None)
    user_data = None
    if user_name:
        user_data = get_user_info(user_name)

    # Search in twitter api.
    users = search_users(name)
    return render_template("tweets.html", users=users, user_data=user_data)


@tweets_app.route("/post/<text>")
def post_tweet(text):

    oauth_token = request.cookies.get('oauth_token')
    oauth_token_secret = request.cookies.get('oauth_token_secret')

    api_resp = post_new_tweet(text, oauth_token, oauth_token_secret)

    api_resp = json.loads(api_resp)

    print(api_resp, type(api_resp))

    # {"errors":[{"code":187,"message":"Status is a duplicate."}]}
    errors = None
    if u"errors" in api_resp:
        errors = api_resp

    return render_template("tweet_posted.html", errors=errors)
