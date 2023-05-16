import os
from pathlib import Path

path = Path(__file__).parent
SQLITE_DEV = "sqlite:///" + str(path / "api_dev.db")
SQLITE_TEST = "sqlite:///" + str(path / "api_test.db")
SQLITE_PROD = "sqlite:///" + str(path / "api_prod.db")

LOG_TO_STDOUT = (None,)

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/{}"
default_db = "multi-tenancy-test"


class Config:
    """Base configuration."""

    LOG_TO_STDOUT = (None,)
    SECRET_KEY = os.getenv("SECRET_KEY", "my_super_secret_key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    KC_BASE_URL = os.getenv("KC_BASE_URL", "http://localhost:8080")
    KC_REALM = os.getenv("KC_REALM", "master")
    KC_TOKEN_ENDPOINT = os.getenv(
        "KC_TOKEN_ENDPOINT",
        f"http://localhost:8080/realms/{KC_REALM}/openid-connect/token",
    )

    # SQLALCHEMY_BINDS = SQLALCHEMY_DATABASE_URI.format(default_db)


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = SQLITE_TEST
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {
            "check_same_thread": False,
        },
    }


class DevelopmentConfig(Config):
    """Development configuration."""

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", SQLITE_DEV)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """Production configuration."""

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", SQLITE_PROD)
    PRESERVE_CONTEXT_ON_EXCEPTION = True


ENV_CONFIG_DICT = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig,
)


def get_config(config_name):
    """Retrieve environment configuration settings."""
    return ENV_CONFIG_DICT.get(config_name, ProductionConfig)
