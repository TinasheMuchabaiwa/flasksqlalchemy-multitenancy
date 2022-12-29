from app import create_app, db
from app.models.user import User


app = create_app("development")


@app.shell_context_processor
def shell():
    return {
        "db": db,
        "User": User,
    }
