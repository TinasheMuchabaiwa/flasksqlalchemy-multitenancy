from http import HTTPStatus

from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_restx import abort

from app.api import keycloak_openid
from app.models.user import User

basic_auth = HTTPBasicAuth()


@basic_auth.verify_password
def verify_password(username, password):
    if not username or not password:
        abort(
            HTTPStatus.UNAUTHORIZED,
            "username or password is missing",
            status="fail",
        )

    user = User.query.filter_by(username=username).first()
    if user:
        if not user.valid_token():
            token = keycloak_openid.token(username=username, password=password)
            user.token = token
        return user


@basic_auth.error_handler
def basic_auth_error(error):
    abort(
        HTTPStatus.UNAUTHORIZED,
        "username or password does not match",
        status="fail",
    )


token_auth = HTTPTokenAuth()


@token_auth.verify_token
def verify_token(token):
    if not token:
        abort(
            HTTPStatus.UNAUTHORIZED,
            "Token is missing",
            status="fail",
        )

    return User.check_token(token) if token else None


@token_auth.error_handler
def token_auth_error(status):
    abort(
        HTTPStatus.UNAUTHORIZED,
        "Token does not match",
        status="fail",
    )
