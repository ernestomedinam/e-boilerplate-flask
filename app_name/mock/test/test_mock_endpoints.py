import pytest
from app_name.conftest import json_header

def test_success_mock_crud_requests(api_client):
    """
        test mock is crud correctly using endpoints.
    """
    request_body = {
        "name": "Some name",
        "parts": 2,
        "description": "trying to create from endpoint!"
    }
    response = api_client.tramit(
        method="post",
        path="mocks",
        json=request_body,
        headers=json_header
    )
    assert response.status_code == 201
    assert request_body["name"] == response.json["name"]
    mock_id = response.json["id"]
    # test object can be updated
    request_body.pop("name")
    request_body["parts"] = 8
    request_body["description"] = "updated description"
    response = api_client.tramit(
        method="patch",
        path=f"mocks/{mock_id}",
        json=request_body,
        headers=json_header
    )
    assert response.status_code == 200
    assert request_body["description"] == response.json["description"]
    assert response.json["parts"] == 8
    # test get specific object
    response = api_client.tramit(
        path=f"mocks/{mock_id}",
        headers=json_header
    )
    assert response.status_code == 200
    assert response.json["id"] == mock_id
    # test get list of objects
    request_body["name"] = "A new object"
    api_client.tramit(
        method="post",
        path="mocks",
        json=request_body,
        headers=json_header
    )
    response = api_client.tramit(
        path="mocks",
        headers=json_header
    )
    assert response.status_code == 200
    assert len(response.json) == 2
    # test delete object
    response = api_client.tramit(
        method="delete",
        path=f"mocks/{mock_id}",
        headers=json_header
    )
    assert response.status_code == 204

def test_wrong_mock_crud_requests(api_client):
    """ test some wrong cruds requests """
    # create without required
    request_body = {
        "name": "good name",
        "parts": 5
    }
    response = api_client.tramit(
        method="post",
        path="mocks",
        json=request_body,
        headers=json_header
    )
    assert response.status_code == 400
    assert "required" in response.json
    # test can't update empty name
    request_body["description"] = "some description here..."
    response = api_client.tramit(
        method="post",
        path="mocks",
        json=request_body,
        headers=json_header
    )
    assert response.status_code == 201
    mock_id = response.json["id"]
    request_body = {
        "name": ""
    }
    response = api_client.tramit(
        method="patch",
        path=f"mocks/{mock_id}",
        json=request_body,
        headers=json_header
    )
    assert response.status_code == 400
    # test not found for patch or delete
    response = api_client.tramit(
        method="patch",
        path=f"mock/0",
        json=request_body,
        headers=json_header
    )
    assert response.status_code == 404
