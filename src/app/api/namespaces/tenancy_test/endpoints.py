from http import HTTPStatus

from flask_restx import Namespace, Resource

from app.api.namespaces.tenancy_test.business import (
    create_organization,
    create_user,
)
from app.api.namespaces.tenancy_test.dto import (
    org_req_parser,
    org_model,
    org_pagination_model,
    user_req_parser,
    user_model,
    user_pagination_model,
)
from uuid import uuid4

abc_ns = Namespace(
    name="abc",
    description="abc",
    validate=True
)

abc_ns.models[org_model.name] = org_model
abc_ns.models[org_pagination_model.name] = org_pagination_model
abc_ns.models[user_model.name] = user_model
abc_ns.models[user_pagination_model.name] = user_pagination_model


@abc_ns.route("/organization", endpoint="organization")
@abc_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@abc_ns.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@abc_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internalserver error")
class OrganizationList(Resource):
    @abc_ns.expect(org_req_parser, validate=True)
    @abc_ns.response(int(HTTPStatus.CREATED), "Success")
    def post(self):
        """Create a new organization"""
        data = org_req_parser.parse_args()
        return create_organization(data)

    # @abc_ns.response(int(HTTPStatus.OK), "Success", org_pagination_model)
    # def get(self):
    #     """List all organizations"""
    #     return {"items": []}, HTTPStatus.OK


@abc_ns.route("/user", endpoint="user")
@abc_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@abc_ns.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@abc_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internalserver error")
class UserList(Resource):
    @abc_ns.expect(user_req_parser, validate=True)
    @abc_ns.response(int(HTTPStatus.CREATED), "Success")
    def post(self):
        """Create a new user"""
        data = user_req_parser.parse_args()
        data["id"] = str(uuid4())
        return create_user(data)

    # @abc_ns.response(int(HTTPStatus.OK), "Success", user_pagination_model)
    # def get(self):
    #     """List all users"""
    #     return {"items": []}, HTTPStatus.OK
