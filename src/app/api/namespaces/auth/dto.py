from flask_restx.reqparse import RequestParser

auth_req_parser = RequestParser(bundle_errors=True)
auth_req_parser.add_argument(
    name="username", type=str, location="form", required=True, nullable=False
)
auth_req_parser.add_argument(
    name="password", type=str, location="form", required=True, nullable=False
)
