import json
from flask import Blueprint, make_response, request
from app_name.mock.models import Mock

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
    headers = {
        "Content-Type": "application/json"
    }
    response = {
        "status_code": 404,
        "text": ""
    }
    if request.headers.get("Content-Type") == headers["Content-Type"]:
        if request.method == "GET":
            if mock_id is not None:
                mock_instance = Mock.query.filter_by(
                    id=mock_id
                ).one_or_none()
                if mock_instance is not None:
                    # return specific mock
                    response["status_code"] = 200
                    response["text"] = mock_instance.serialize()
                else:
                    # no such mock
                    # response["status_code"] = 404
                    pass
            else:
                # return mock list
                mock_list = Mock.query.all()
                serialized_list = []
                [serialized_list.append(mock.serialize()) for mock in mock_list]
                response["status_code"] = 200
                response["text"] = serialized_list

        elif request.method == "POST":
            input_data = request.json
            response = Mock.create(input_data)
            
        elif request.method == "PATCH":
            input_data = request.json
            mock_instance = Mock.query.filter_by(
                id=mock_id
            ).one_or_none()
            if mock_instance is not None:
                # update mock
                response = mock_instance.update(input_data)
            else:
                # no such mock
                # response["status_code"] = 404
                pass

        elif request.method == "DELETE":
            mock_instance = Mock.query.filter_by(
                id=mock_id
            ).one_or_none()
            if mock_instance is not None:
                # delete mock
                response = Mock.delete(mock_instance.id)
            else:
                # no such mock
                # response["status_code"] = 404
                pass
    else:
        # other content type was received
        response["status_code"] = 400
        response["text"] = "this is json content type endpoint."
                
    return make_response(
        json.dumps(response["text"]),
        response["status_code"],
        headers
    )