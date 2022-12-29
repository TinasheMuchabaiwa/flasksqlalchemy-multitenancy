from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


from app import api
from app.config import get_config

db = SQLAlchemy()
migrate = Migrate()


def create_app(app_config=None):
    app = Flask(__name__)

    if app_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_object(get_config(app_config))

    db.init_app(app)
    migrate.init_app(app, db)

    # Ensure FOREIGN KEY for sqlite3
    if "sqlite" in app.config["SQLALCHEMY_DATABASE_URI"]:

        def _fk_pragma_on_connect(dbapi_con, con_record):  # noqa
            dbapi_con.execute("pragma foreign_keys=ON")

        with app.app_context():
            from sqlalchemy import event

            event.listen(db.engine, "connect", _fk_pragma_on_connect)

    api.init_app(app)

    return app
