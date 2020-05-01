# config tests for api blueprint enpoints
import os
import pytest

def test_api_is_up(client):
    """ test api is up and running, no auth, no nothing. """
    def test_hello(client):
        response = client.get("api/hello")
        assert "result" in response.json
        assert response.status_code == 200
