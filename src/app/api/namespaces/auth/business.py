from http import HTTPStatus

from flask import jsonify
from flask_restx import abort

from app import db
from app.api.namespaces.auth import basic_auth


def process_login_request():
    user = basic_auth.current_user()
    if not user:
        abort(
            HTTPStatus.UNAUTHORIZED,
            "username or password does not match",
            status="fail",
        )

    token = user.get_token()
    db.session.add(user)
    db.session.commit()
    return _create_auth_successful_response(
        token=token, status_code=HTTPStatus.OK, message="successfully logged in"
    )


def _create_auth_successful_response(token, status_code, message):
    token["message"] = message
    token["status"] = "success"
    response = jsonify(**token)
    response.status_code = status_code
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    return response
