# config tests for flask app in different scenarios
import os
import pytest
from app_name import create_app

def test_config(app):
    assert not create_app().testing
    assert app.config["TESTING"] == True
    assert app.config["ENV"] == "development"
    assert app.config["DEBUG"] == True

def test_dev_config():
    app = create_app()
    assert app.config["ENV"] == "development"
    assert app.config["DEBUG"] == True