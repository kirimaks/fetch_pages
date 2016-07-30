from flask import Blueprint

tweets_app = Blueprint('tweets', __name__)

from . import views
