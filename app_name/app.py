from flask import Flask
from flask_cors import CORS

from config import app_config

from app_name.db import db, migrate
from app_name.api import rest_api, docs, spec


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object("app_name.settings")
    app.config.from_object(app_config.config[config_name])
    app_config.config[config_name].init_app(app)
    app.config.update({"APISPEC_SPEC": spec})

    with app.app_context():

        import app_name.mock.routes

        rest_api.init_app(app)

        CORS(app, supports_credentials=True)

        # uncomment to init jwt app
        # jwt.init_app(app)

        db.init_app(app)
        migrate.init_app(app, db)
        
        docs.init_app(app)

        return app
