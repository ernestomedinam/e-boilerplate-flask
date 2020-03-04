import os
import json
from flask import Flask, make_response
from config import config

def create_app(config_name="development"):
    """ create and configure flask app """
    # return app with config file on config folder
    app = Flask(__name__)

    # get default settings for app
    app.config.from_object("src.settings")

    # load according config object
    app.config.from_object(config.config[config_name])

    # run classmethod to init app with Flask-DotEnv
    config.config[config_name].init_app(app)

    # add ad-hoc config from mapping
    # app.config.from_mapping(
    #     SECRET_KEY="dev"
    # )

    @app.route("/hello")
    def welcome():
        """ endpoint to check if api is up """
        headers = {
            "Content-Type": "application/json"
        }
        response_body = {
            "result": "HTTP_200_OK. hello, fellow surfer"
        }
        status_code = 200
        print(app.config)
        return make_response(
            json.dumps(response_body),
            status_code,
            headers
        )

    return app