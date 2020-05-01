import json
from flask import Blueprint, make_response, request

mock_module = Blueprint("mock", __name__)

@mock_module.route("/mocks", methods=["GET", "POST"])
@mock_module.route("/mocks/<mock_id>", methods=["GET", "PATCH", "DELETE"])
def handle_mocks(mock_id = None):
    """
        handle mock endpoints requests:
            GET     mocks/: list of mocks
            POST    mocks/: create new mock
            GET     mocks/<mock_id>: mock details
            PATCH   mocks/<mock_id>: partially update a mock
            DELETE  mocks/<mock_id>: delete a mock
    """
    # 501 working on it response
    response = {
        "status_code": 501,
        "text": "working on it, coming soon..."
    }
    if request.method == "GET":
        pass
    elif request.method == "POST":
        pass
    elif request.method == "PATCH":
        pass
    elif request.method == "DELETE":
        pass
    return make_response(
        json.dumps(response["text"]),
        response["status_code"]
    )