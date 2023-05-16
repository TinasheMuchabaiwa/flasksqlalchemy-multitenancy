import os

from flask import Blueprint, Flask
from flask_restx import Api
# from keycloak import KeycloakOpenID, KeycloakAdmin

bp = Blueprint("api", __name__, url_prefix="/api/v1")

authorizations = {
    "Basic": {
        "type": "basic",
        "flow": "password",
    },
    "Bearer": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
    },
}

api = Api(
    app=bp,
    title="title",
    description="description",
    authorizations=authorizations,
)

# keycloak_openid = KeycloakOpenID(
#     server_url=os.getenv("KC_BASE_URL"),
#     realm_name=os.getenv("KC_REALM"),
#     client_id=os.getenv("KC_CLIENT_ID"),
#     client_secret_key=os.getenv("KC_CLIENT_SECRET"),
# )

# keycloak_admin = KeycloakAdmin(
#     server_url=os.getenv("KC_BASE_URL"),
#     realm_name=os.getenv("KC_REALM"),
#     username=os.getenv("KC_ADMIN_USERNAME"),
#     password=os.getenv("KC_ADMIN_PASSWORD"),
#     client_id=os.getenv("KC_CLIENT_ID"),
#     client_secret_key=os.getenv("KC_CLIENT_SECRET"),
#     verify=True,
# )


def init_app(app: Flask):
    app.register_blueprint(blueprint=bp)

    # from app.api.namespaces.users.endpoints import user_ns
    # from app.api.namespaces.auth.endpoints import auth_ns
    from app.api.namespaces.tenancy_test.endpoints import abc_ns

    # api.add_namespace(user_ns)
    # api.add_namespace(auth_ns)
    api.add_namespace(abc_ns)
