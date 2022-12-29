import base64
from http import HTTPStatus
from unittest.mock import patch

from flask import url_for

from app.models.user import User
from tests.util import USERNAME_ADMIN, PASSWORD

SUCCESS = "successfully logged in"
UNAUTHORIZED = "username or password does not match"


def login_user(test_client, username=USERNAME_ADMIN, password=PASSWORD):
    credentials = f"{username}:{password}".encode("ascii")
    valid_credentials = base64.b64encode(credentials).decode("utf-8")
    return test_client.post(
        url_for("api.auth_login"),
        headers={"Authorization": "Basic " + valid_credentials},
    )


@patch("app.api.keycloak_openid.token")
@patch("app.api.keycloak_admin.send_verify_email")
@patch("app.api.keycloak_admin.create_user")
def test_login(create_user_mock, send_email_mock, token_mock, client, db, user):

    create_user_mock.return_value = "XXXX"
    send_email_mock.return_value = True
    token_mock.return_value = {"access_token": "XXX", "expires_in": 60}

    response = login_user(client)
    assert response.status_code == HTTPStatus.OK
    assert "status" in response.json and response.json["status"] == "success"
    assert "message" in response.json and response.json["message"] == SUCCESS
    assert "access_token" in response.json
    user = User.find_by_username(USERNAME_ADMIN)
    assert user and user.username == USERNAME_ADMIN


def test_login_username_does_not_exist(client, db):
    response = login_user(client)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert "message" in response.json and response.json["message"] == UNAUTHORIZED
    assert "access_token" not in response.json
