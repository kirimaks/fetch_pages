import oauth2
import json

API_KEY = 'U26cgDp3zOj7p84VJpwDHoY7B'
API_SECRET = 'vudQQfkWj0QriPaZagYyVD90T2vmeLrCZOPfpzufwzghBPh9Uk'
TOKEN_KEY = '745349279326281730-vx9LQIJpJsbEsa0WUdoKn9TrmTUBqee'
TOKEN_SERCRET = '631dYS20bMctP7UIEbZwUZQZDx9KTVNbO6azaZT86NiNj'

url_pattern = "https://api.twitter.com/1.1/search/tweets.json?q=%23{}&lang=en&result_type=popular&count=20"


def oauth_req(url, key, secret, http_method="GET",
              post_body="", http_headers=None):
    consumer = oauth2.Consumer(key=API_KEY, secret=API_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request(url, method=http_method,
                                   body=post_body, headers=http_headers)

    return content


def get_tweets(tag):
    if tag is None:
        return []

    if tag.startswith("#"):
        tag = tag.lstrip("#")

    url = url_pattern.format(tag)
    data = oauth_req(url, TOKEN_KEY, TOKEN_SERCRET)
    buff = list()

    for status in json.loads(data)['statuses']:
        buff.append(status)

    return buff


def search_users(name):
    if name:
        url = "https://api.twitter.com/1.1/users/search.json?q={}".format(name)
        data = oauth_req(url, TOKEN_KEY, TOKEN_SERCRET)
        users = [user['screen_name'] for user in json.loads(data)]
        return users[:12]
    return []
