import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy.orm.scoping import ScopedSession

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
            db.create_all()
            event.listen(db.engine, "connect", _fk_pragma_on_connect)

    api.init_app(app)

    return app


# def get_tenant_session(tenant: str):
#     prepare_bind(get_bind_key(tenant))
#     engine = db.get_engine(create_app(), bind=get_bind_key(tenant))
#     session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
#     return session


# def prepare_bind(bind_key):
#     pg_url = get_config("development").SQLALCHEMY_DATABASE_URI
#     if bind_key not in get_config("development").SQLALCHEMY_BINDS:
#         get_config("development").SQLALCHEMY_BINDS[bind_key] = pg_url.format(bind_key)


# def get_bind_key(tenant):
#     if tenant.has_own_db:
#         return tenant.db_name
#     return "default"


# db.session = get_tenant_session(tenant=tenant_object)