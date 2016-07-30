from flask import Blueprint

login_app = Blueprint('login', __name__)

from . import views
