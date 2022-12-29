import json
from http import HTTPStatus

from flask_restx import Namespace, Resource
from keycloak import KeycloakPostError, KeycloakAuthenticationError

from app import db
from app.api.namespaces.auth import basic_auth, token_auth
from app.api.namespaces.auth.business import process_login_request
from app.api.namespaces.users.dto import user_model

auth_ns = Namespace(
    name="auth", description="Authentication and authorization management", validate=True
)
auth_ns.models[user_model.name] = user_model


@auth_ns.errorhandler(KeycloakAuthenticationError)
@auth_ns.errorhandler(KeycloakPostError)
def specific_namespace_error_handler(error):
    """Namespace error handler"""
    error_json = json.loads(error.response_body.decode("utf-8"))
    if "error_description" in error_json:
        message = error_json["error_description"]
    else:
        message = error_json["errorMessage"]
    return {"message": message}, getattr(error, "response_code", 409)


@auth_ns.route("/login", endpoint="auth_login")
@auth_ns.doc(security="Basic")
class Login(Resource):
    @auth_ns.response(int(HTTPStatus.OK), "Login succeeded.")
    @auth_ns.response(int(HTTPStatus.UNAUTHORIZED), "email or password does not match")
    @auth_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @auth_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    @basic_auth.login_required
    def post(self):
        """Authenticate an existing user and return an access token."""
        return process_login_request()


@auth_ns.route("/logout", endpoint="auth_logout")
class Logout(Resource):
    @auth_ns.response(int(HTTPStatus.NO_CONTENT), "Logout succeeded.")
    @auth_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token does not match")
    @auth_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @auth_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    @auth_ns.doc(security="Bearer")
    @token_auth.login_required
    def delete(self):
        token_auth.current_user().revoke_token()
        db.session.commit()
        return "", 204
