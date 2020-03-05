import os
import pytest
from app_name import create_app

# declare fixture for app so tests get app with testing = True
@pytest.fixture
def app():
    app = create_app("testing")

    with app.app_context():
        pass

    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()