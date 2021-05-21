import os
import io
import pytest

from app_name.app import create_app
from app_name.db import db


# declare fixture for app so tests get app with testing = True
@pytest.fixture(scope="session")
def app():
    app = create_app("test")
    app.testing = True
    with app.app_context():
        yield app


# fixture for pytest-flask-sqlalchemy
@pytest.fixture(scope="function")
def _db(app):
    with app.app_context():

        yield db


# fixture to use an api_client, no db integration
@pytest.fixture(scope="function")
def client(app, db_session):
    with app.test_client() as _client:
        api_client = APIResource(_client, "api")
        yield api_client


# helper Resource class
class APIResource():
    def __init__(self, app_client, prefix):
        # init app client
        self.app_client = app_client
        self.prefix = prefix.strip("/")
        self.headers = { "Content-Type": "application/json" }

    def _delegate(self, method, path="", *args, **kwargs):
        # grab method fn
        app_client_fn = getattr(self.app_client, method)
        # prefix endpoint
        prefixed_path = os.path.join(self.prefix, path)
        # fetch
        return app_client_fn(prefixed_path, headers=self.headers, *args, **kwargs)

    def fetch(self, method="get", headers={}, *args, **kwargs):
        for (header, value) in headers.items():
            self.headers[header] = value
        return self._delegate(method, *args, **kwargs)
