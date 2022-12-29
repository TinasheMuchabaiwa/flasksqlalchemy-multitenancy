from flask_restx import Model
from flask_restx.fields import String
from flask_restx.inputs import positive
from flask_restx.reqparse import RequestParser

pagination_req_parser = RequestParser(bundle_errors=True)
pagination_req_parser.add_argument(
    "page", location="args", type=positive, required=False, default=1
)
pagination_req_parser.add_argument(
    "per_page",
    location="args",
    type=positive,
    required=False,
    choices=[5, 10, 25, 50, 100],
    default=10,
)

pagination_links_model = Model(
    "Nav Links",
    {
        "self": String,
        "prev": String,
        "next": String,
        "first": String,
        "last": String,
    },
)
