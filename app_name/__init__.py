import os
import json
from flask import Flask, make_response
from flask_migrate import Migrate
from config import app_config
from app_name.api.routes import api_mod
from app_name.db import db 

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

    # init db instance
    db.init_app(app)

    # migrate  for Flask-Migrate
    migrate = Migrate(app, db)

    return app