import os
import pytest
from app_name import create_app
from app_name.db import db, migrate

# declare fixture for app so tests get app with testing = True
@pytest.fixture(scope="module")
def app():
    app = create_app("testing")
    with app.app_context():
        yield app

# required fixtures for pytest-flask-sqlalchemy
@pytest.fixture(scope="module")
def _db(app):
    with app.app_context():
        # start app and db for app as new empty db for session
        db.init_app(app)
        migrate.init_app(app, db)
        db.drop_all()
        db.create_all()
    
        return db

# fixture to use an api_client
@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(scope="function")
def api_client(app, db_session):
    _api_client = BlueprintClient(
        app.test_client(),
        "api"
    )
    yield _api_client


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

# helper blueprint class
class BlueprintClient():
    def __init__(self, app_client, blueprint_url_prefix):
        # init app client
        self.app_client = app_client
        self.blueprint_url_prefix = blueprint_url_prefix.strip("/")

    def _delegate(self, method, path="", *args, **kwargs):
        app_client_function = getattr(self.app_client, method)
        prefixed_path = os.path.join(self.blueprint_url_prefix, path)
        return app_client_function(prefixed_path, *args, **kwargs)

    def tramit(self, method="get", *args, **kwargs):
        return self._delegate(method, *args, **kwargs)

# helper basic header variable:
json_header = {
    "Content-Type": "application/json"
}