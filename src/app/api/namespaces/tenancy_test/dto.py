from flask_restx import Model
from flask_restx.fields import Integer, String, Boolean, Nested, List
from flask_restx.reqparse import RequestParser

from app.api.dto import pagination_links_model

org_req_parser = RequestParser(bundle_errors=True)
org_req_parser.add_argument(
    name="name", type=str, location="json", required=True, nullable=False
)

org_model = Model(
    "Component",
    {
        "name": String,
    },
)


org_pagination_model = Model(
    "OrganizationPagination",
    {
        "links": Nested(pagination_links_model, skip_none=True),
        "has_prev": Boolean,
        "has_next": Boolean,
        "page": Integer,
        "total_pages": Integer(attribute="pages"),
        "items_per_page": Integer(attribute="per_page"),
        "total_items": Integer(attribute="total"),
        "items": List(Nested(org_model)),
    },
)

user_req_parser = RequestParser(bundle_errors=True)
user_req_parser.add_argument(
    name="name", type=str, location="json", required=True, nullable=False
)
user_req_parser.add_argument(
    name="organization_id", type=int, location="json", required=True, nullable=False
)

user_model = Model(
    "User",
    {
        "name": String,
        "organization_id": Integer,
        "id": String,
    }
)

user_pagination_model = Model(
    "UserPagination",
    {
        "links": Nested(pagination_links_model, skip_none=True),
        "has_prev": Boolean,
        "has_next": Boolean,
        "page": Integer,
        "total_pages": Integer(attribute="pages"),
        "items_per_page": Integer(attribute="per_page"),
        "total_items": Integer(attribute="total"),
        "items": List(Nested(user_model)),
    }
)
