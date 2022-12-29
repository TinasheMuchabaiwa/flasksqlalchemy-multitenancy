from flask_restx import Model
from flask_restx.fields import Nested, Boolean, Integer, List, String, Url
from flask_restx.inputs import email
from flask_restx.reqparse import RequestParser

from app.api.dto import pagination_links_model

user_req_parser = RequestParser(bundle_errors=True)
user_req_parser.add_argument(
    name="username", type=str, location="json", required=True, nullable=False
)
user_req_parser.add_argument(
    name="first_name", type=str, location="json", required=True, nullable=False
)
user_req_parser.add_argument(
    name="last_name", type=str, location="json", required=True, nullable=False
)
user_req_parser.add_argument(
    name="email", type=email(), location="json", required=True, nullable=False
)
user_req_parser.add_argument(
    name="enabled", type=bool, location="json", required=True, nullable=False
)


user_model = Model(
    "User",
    {
        "username": String,
        "first_name": String,
        "last_name": String,
        "email": String,
        "enabled": Boolean,
        "link": Url("api.user", absolute=True),
    },
)


user_pagination_model = Model(
    "Pagination",
    {
        "links": Nested(pagination_links_model, skip_none=True),
        "has_prev": Boolean,
        "has_next": Boolean,
        "page": Integer,
        "total_pages": Integer(attribute="pages"),
        "items_per_page": Integer(attribute="per_page"),
        "total_items": Integer(attribute="total"),
        "items": List(Nested(user_model)),
    },
)
