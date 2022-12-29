from http import HTTPStatus

from flask_restx import Namespace, Resource

from app.api.dto import pagination_req_parser
from app.api.namespaces.auth import token_auth
from app.api.namespaces.users.business import (
    retrieve_user_list,
    create_user,
    retrieve_user,
    update_user,
    delete_user,
)
from app.api.namespaces.users.dto import (
    user_pagination_model,
    user_req_parser,
    user_model,
)

user_ns = Namespace(name="user", description="User Management", validate=True)
user_ns.models[user_model.name] = user_model
user_ns.models[user_pagination_model.name] = user_pagination_model


@user_ns.route("", endpoint="user_list")
@user_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@user_ns.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@user_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class UserList(Resource):
    """Handles HTTP requests to URL: /user."""

    @user_ns.expect(pagination_req_parser)
    @user_ns.response(HTTPStatus.OK, "Retrieved user list.", user_pagination_model)
    @user_ns.doc(security="Bearer")
    @token_auth.login_required
    def get(self):
        """Retrieve a list of users."""
        request_data = pagination_req_parser.parse_args()
        page = request_data.get("page")
        per_page = request_data.get("per_page")
        return retrieve_user_list(page, per_page)

    @user_ns.expect(user_req_parser)
    @user_ns.response(int(HTTPStatus.CREATED), "New user added.")
    @user_ns.response(int(HTTPStatus.FORBIDDEN), "Valid token required.")
    @user_ns.response(int(HTTPStatus.CONFLICT), "User already exists.")
    @user_ns.doc(security="Bearer")
    @token_auth.login_required
    def post(self):
        """Create a user."""
        user_data = user_req_parser.parse_args()
        return create_user(user_data)


@user_ns.route("/<int:id>", endpoint="user")
@user_ns.param("id", "User ID")
@user_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@user_ns.response(int(HTTPStatus.NOT_FOUND), "User not found.")
@user_ns.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@user_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class User(Resource):
    """Handles HTTP requests to URL: /user/{id}."""

    @user_ns.response(int(HTTPStatus.OK), "Retrieved user.", user_model)
    @user_ns.marshal_with(user_model)
    @user_ns.doc(security="Bearer")
    @token_auth.login_required
    def get(self, id):
        """Retrieve a link type."""
        return retrieve_user(id)

    @user_ns.expect(user_req_parser)
    @user_ns.response(int(HTTPStatus.OK), "User was updated.", user_model)
    @user_ns.response(int(HTTPStatus.CREATED), "New user added.")
    @user_ns.response(int(HTTPStatus.FORBIDDEN), "Valid token required.")
    @user_ns.doc(security="Bearer")
    @token_auth.login_required
    def put(self, id):
        """Update a user."""
        user_data = user_req_parser.parse_args()
        return update_user(id, user_data)

    @user_ns.response(int(HTTPStatus.NO_CONTENT), "User was deleted.")
    @user_ns.response(int(HTTPStatus.FORBIDDEN), "Valid token required.")
    @user_ns.doc(security="Bearer")
    @token_auth.login_required
    def delete(self, id):
        """Delete a user."""
        return delete_user(id)
