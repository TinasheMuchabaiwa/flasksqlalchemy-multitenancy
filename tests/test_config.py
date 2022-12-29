import os

from app import create_app
from app.config import SQLITE_DEV, SQLITE_TEST, SQLITE_PROD


def test_config_development():
    app = create_app("development")
    assert app.config["SECRET_KEY"] != "my_super_secret_key"
    assert not app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == os.getenv("DATABASE_URL", SQLITE_DEV)


def test_config_testing():
    app = create_app("testing")
    assert app.config["SECRET_KEY"] != "my_super_secret_key"
    assert app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == SQLITE_TEST


def test_config_production():
    app = create_app("production")
    assert app.config["SECRET_KEY"] != "my_super_secret_key"
    assert not app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == os.getenv(
        "DATABASE_URL", SQLITE_PROD
    )
