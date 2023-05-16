import os

from dotenv import load_dotenv

base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, ".env"))

from app import create_app, db  # noqa
from app.api.namespaces.tenancy_test.models import User, Organization  # noqa

app = create_app("development")


@app.shell_context_processor
def shell():
    return {
        "db": db,
        "User": User,
        "Compaby": Organization,
    }
