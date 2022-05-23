import pytest
from flask import session, g

from comments.db import get_db


@pytest.mark.parametrize(
    ("email", "username", "password", "message"),
    (
            ("", "", "", b"Email is required."),
            ("test.user@gmail.com", "", "", b"Username is required."),
            ("test.user@gmail.com", "test_user", "", b"Password is required."),
            ("other.user@gmail.com", "other_user2", "Other_user_password1",
             b"User other_user2 or Email other.user@gmail.com is already registered."),
            ("test.user@163.com", "test_user", "Test_user_password1",
             b"User test_user or Email test.user@163.com is already registered."),
    ),
)
def test_signup_validate_input(client, email, username, password, message):
    response = client.post(
        "/signup", data={"email": email, "username": username, "password": password}
    )
    assert message in response.data


def test_signup(client, app):
    assert client.get("/signup").status_code == 200

    response = client.post("/signup", data={"username": "test_user2", "email": "test.user2@gamil.com",
                                            "password": "Test_user_password2"})
    assert response.headers["Location"] == "/login"

    with app.app_context():
        assert get_db().execute("SELECT * FROM user WHERE username = 'test_user2'").fetchone() is not None


@pytest.mark.parametrize(
    ("email", "username", "password", "message"),
    (
            ("", "", "", b"Username or Email must has one."),
            ("test.user@gmail.com", "test_user", "Other_user_password1", b"Username or Email just need one"),
            ("", "other_user2", "Other_user_password1", b"Incorrect username."),
            ("", "test_user", "test", b"Incorrect password."),
    ),
)
def test_login_validate_input(client, email, username, password, message):
    response = client.post(
        "/login", data={"email": email, "username": username, "password": password}
    )
    assert message in response.data


def test_login(client, auth):
    assert client.get("/login").status_code == 200

    # username + password
    response = client.post("/login", data={"username": 'test_user', "password": 'Test_user_password1'})
    assert response.headers["Location"] == "/"
    client.get('/logout')

    # email + password
    response = client.post("/login", data={"email": 'test.user@gmail.com', "password": 'Test_user_password1'})
    assert response.headers["Location"] == "/"

    with client:
        response = client.get("/")
        assert session["user_id"] == 1
        assert g.user["username"] == "test_user"
        # 页面显示用户名和 Email
        assert b"test_user" in response.data
        assert b"test.user@gmail.com" in response.data
