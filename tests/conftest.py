import os
import tempfile

import pytest
from comments import create_app
from comments.db import init_db, get_db

with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture()
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({"TESTING": True, "DATABASE": db_path})

    # other setup can go here
    # app.app_context() 用于 g
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    # clean up / reset resources here
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture
def auth(client):
    return AuthActions(client)


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username="test_user", password="Test_user_password1"):
        return self._client.post("/login", data={"username": username, "password": password})
