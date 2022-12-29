from http import HTTPStatus

from flask import jsonify, url_for
from flask_restx import marshal, abort

from app import db
from app.api import keycloak_admin
from app.api.business import _pagination_nav_links, _pagination_nav_header_links
from app.api.namespaces.users.dto import user_pagination_model
from app.models.user import User


def create_user(user_data: dict):
    email = user_data["email"]

    if User.find_by_email(email=email):
        error = f"User {email} already exists, must be unique."
        abort(HTTPStatus.CONFLICT, error, status="fail")

    username = user_data["username"]
    first_name = user_data["first_name"]
    last_name = user_data["last_name"]
    enabled = user_data["enabled"]

    keycloak_user = keycloak_admin.create_user(
        {
            "email": email,
            "username": username,
            "firstName": first_name,
            "lastName": last_name,
            "enabled": enabled,
        },
        exist_ok=False,
    )
    keycloak_admin.send_verify_email(user_id=keycloak_user)

    user = User(
        username=username,
        email=email,
        kc_user_id=keycloak_user,
        admin=False,
    )
    db.session.add(user)
    db.session.commit()

    response = jsonify(status="success", message=f"New user added: {user.email}.")
    response.status_code = HTTPStatus.CREATED
    response.headers["Location"] = url_for("api.user", id=user.id, _external=True)
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    return response


def retrieve_user_list(page: int, per_page: int):
    pagination = User.query.paginate(page, per_page, error_out=False)
    response_data = marshal(pagination, user_pagination_model)
    response_data["links"] = _pagination_nav_links(pagination, "api.user_list")
    response = jsonify(response_data)
    response.headers["Link"] = _pagination_nav_header_links(pagination, "api.user_list")
    response.headers["Total-Count"] = pagination.total
    return response


def retrieve_user(user_id: int):
    return User.query.filter_by(id=user_id).first_or_404(
        description="User not found in database."
    )


def update_user(user_id: int, user_data: dict):
    user = User.filter_by(id=user_id).first()
    if user:
        for k, v in user_data.items():
            setattr(user, k, v)
        db.session.commit()
        message = f"'User: {user.email}' was successfully updated"
        response_dict = dict(status="success", message=message)
        return response_dict, HTTPStatus.OK

    abort(HTTPStatus.NOT_FOUND, "User not found", status="fail")


def delete_user(user_id: int):
    user = User.query.filter_by(id=user_id).first_or_404(
        description="User not found in database."
    )
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT
