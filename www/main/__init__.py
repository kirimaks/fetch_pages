from flask import Flask, render_template

from config import config, BasicConfig
from search import search_app
from tweets import tweets_app
from login import login_app


# Home controller.
def index():
    return render_template("hello.html")


def create_app(config_name):
    app = Flask(__name__, root_path=BasicConfig.BASE_DIR)
    app.config.from_object(config[config_name])

    # Home page.
    app.add_url_rule('/', 'index', index)

    # Controllers from apps.
    app.register_blueprint(search_app, url_prefix="/search")
    app.register_blueprint(tweets_app, url_prefix="/tweets")
    app.register_blueprint(login_app)

    return app
