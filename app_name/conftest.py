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
        
        db.init_app(app)
        # db.create_engine(app.config["SQLALCHEMY_DATABASE_URI"], {})
        migrate.init_app(app, db)
        db.drop_all()
        db.create_all()
    
        return db

# fixture to use an api_client as a logged in user

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()