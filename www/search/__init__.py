from flask import Blueprint

search_app = Blueprint('search', __name__)

from . import views
