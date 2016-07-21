import oauth2
# import json
from urllib import quote_plus
import urlparse

# from pprint import pprint

API_KEY = 'U26cgDp3zOj7p84VJpwDHoY7B'
API_SECRET = 'vudQQfkWj0QriPaZagYyVD90T2vmeLrCZOPfpzufwzghBPh9Uk'
TOKEN_KEY = '745349279326281730-vx9LQIJpJsbEsa0WUdoKn9TrmTUBqee'
TOKEN_SERCRET = '631dYS20bMctP7UIEbZwUZQZDx9KTVNbO6azaZT86NiNj'


def oauth_req(url, key, secret, http_method="GET",
              post_body="", http_headers=None):
    consumer = oauth2.Consumer(key=API_KEY, secret=API_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)

    resp, content = client.request(url, method=http_method,
                                   body=post_body, headers=http_headers)

    return resp, content


def get_request_token():
    url = "https://api.twitter.com/oauth/request_token"
    callback_url = quote_plus("http://127.0.0.1:5000/tweets")
    http_headers = {"oauth_callback": callback_url}
    resp, data = oauth_req(url, TOKEN_KEY, TOKEN_SERCRET,
                           http_method="POST", http_headers=http_headers)

    return dict(urlparse.parse_qsl(content))



def get_access_token(oauth_verifier, oauth_token):
    url = "https://api.twitter.com/oauth/access_token"
    post_body = "oauth_verifier={}".format(oauth_verifier)
    http_headers = {"Content-Length": str(len(post_body)),
                    "Content-Type": "application/x-www-form-urlencoded",
                    "oauth_token": oauth_token}
    resp, data = oauth_req(url, TOKEN_KEY, TOKEN_SERCRET,
                           http_method="POST", post_body=post_body,
                           http_headers=http_headers)

    return data
