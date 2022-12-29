from http import HTTPStatus
from unittest.mock import patch

from app.models.user import User
from tests.test_auth_login import login_user
from tests.util import register_user, EMAIL, BAD_REQUEST, USERNAME

SUCCESS = f"New user added: {EMAIL}."
EMAIL_ALREADY_EXISTS = f"{EMAIL} is already registered"
USERNAME_ALREADY_EXISTS = f"User {EMAIL} already exists, must be unique."


@patch("app.api.keycloak_openid.token")
@patch("app.api.keycloak_admin.send_verify_email")
@patch("app.api.keycloak_admin.create_user")
def test_auth_register(create_user_mock, send_email_mock, token_mock, client, db, user):
    create_user_mock.return_value = "XXXX"
    send_email_mock.return_value = True
    token_mock.return_value = {"access_token": "XXX", "expires_in": 60}

    response = login_user(client)
    response = register_user(client, response.json["access_token"])
    assert response.status_code == HTTPStatus.CREATED
    assert "status" in response.json and response.json["status"] == "success"
    assert "message" in response.json and response.json["message"] == SUCCESS


@patch("app.api.keycloak_openid.token")
@patch("app.api.keycloak_admin.send_verify_email")
@patch("app.api.keycloak_admin.create_user")
def test_auth_register_email_already_registered(
    create_user_mock, send_email_mock, token_mock, client, db, user
):
    end_user = User(username=USERNAME, email=EMAIL, admin=False, kc_user_id="AAA")
    db.session.add(end_user)
    db.session.commit()

    create_user_mock.return_value = "XXXX"
    send_email_mock.return_value = True
    token_mock.return_value = {"access_token": "XXX", "expires_in": 60}

    response = login_user(client)
    response = register_user(client, response.json["access_token"])
    assert response.status_code == HTTPStatus.CONFLICT
    assert (
        "message" in response.json
        and response.json["message"] == EMAIL_ALREADY_EXISTS
        or "message" in response.json
        and response.json["message"] == USERNAME_ALREADY_EXISTS
    )


@patch("app.api.keycloak_openid.token")
def test_auth_register_invalid_email(token_mock, client):
    token_mock.return_value = {"access_token": "XXX", "expires_in": 60}

    response = login_user(client)

    invalid_email = "first last"
    response = register_user(client, response.json["access_token"], email=invalid_email)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "message" in response.json and response.json["message"] == BAD_REQUEST
    assert "errors" in response.json
    assert "email" in response.json["errors"]
    assert response.json["errors"]["email"] == f"{invalid_email} is not a valid email"
