import json
import pytest

from tests.unit.test_mock import mock_data


def post_mock(_client, **kwargs):
    return _client.fetch(
        method="post",
        path="/api/mocks",
        json={**kwargs}
    )

def test_post_mock(client):
    response = post_mock(client, **mock_data)
    assert response.status_code == 201
    assert "id" in response.json

def test_get_mock(client):
    response = post_mock(client, **mock_data)
    mock_id = response.json["id"]
    response = client.fetch(
        method="get",
        path=f"/api/mocks/{mock_id}"
    )
    print(response)
    assert response.status_code == 200
    assert response.json["id"] == mock_id

def test_get_mocks(client):
    post_mock(client, **mock_data)
    response = post_mock(client, **{
        **mock_data,
        "name": "Another name"    
    })
    response = client.fetch(
        method="get",
        path="/api/mocks"
    )
    assert response.status_code == 200
    assert len(response.json) >= 2

def test_patch_mock(client):
    response = post_mock(client, **mock_data)
    mock_id = response.json["id"]
    response = client.fetch(
        method="patch",
        path=f"/api/mocks/{mock_id}",
        json={
            "parts": 48
        }
    )
    assert response.status_code == 200
    assert response.json["parts"] == 48

def test_delete_mock(client):
    response = post_mock(client, **mock_data)
    mock_id = response.json["id"]
    response = client.fetch(
        method="delete",
        path=f"/api/mocks/{mock_id}"
    )
    assert response.status_code == 204
    response = client.fetch(
        method="get",
        path=f"/api/mocks/{mock_id}"
    )
    assert response.status_code == 404
