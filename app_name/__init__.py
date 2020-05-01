import os
import json
from flask import Flask, make_response
from config import app_config
from app_name.api.routes import api_mod
from app_name.db import db, migrate
from app_name.mock.routes import mock_module

def create_app(config_name="development"):
    """ create and configure flask app """
    # return app with config file on config folder
    app = Flask(__name__)

    # get default settings for app
    app.config.from_object("app_name.settings")

    # load according config object
    app.config.from_object(app_config.config[config_name])

    # run classmethod to init app with Flask-DotEnv
    app_config.config[config_name].init_app(app)

    # register blueprints
    app.register_blueprint(api_mod, url_prefix="/api")
    app.register_blueprint(mock_module, url_prefix="/api")

    with app.app_context():
        if config_name != "testing":
            # init db instance
            db.init_app(app)

            # migrate  for Flask-Migrate
            migrate.init_app(app, db)

        return app