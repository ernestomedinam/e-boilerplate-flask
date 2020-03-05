import json
from flask import Blueprint, make_response

api_mod = Blueprint("api", __name__)

@api_mod.route("/hello")
def hello_api():
    """ endpoint to check if api is up """
    headers = {
        "Content-Type": "application/json"
    }
    response_body = {
        "result": "HTTP_200_OK. hello, fellow surfer"
    }
    status_code = 200
    return make_response(
        json.dumps(response_body),
        status_code,
        headers
    )