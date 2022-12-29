from datetime import timedelta, datetime

import pytest

from app import create_app, db as database
from app.models.user import User
from tests.util import (
    USERNAME_ADMIN,
    EMAIL_ADMIN,
)


@pytest.fixture
def app():
    app = create_app("testing")
    return app


@pytest.fixture
def db(app, client, request):
    database.drop_all()
    database.create_all()
    database.session.commit()

    def fin():
        database.session.remove()

    request.addfinalizer(fin)
    return database


@pytest.fixture
def user(db):
    user = User(
        username=USERNAME_ADMIN,
        email=EMAIL_ADMIN,
        admin=False,
        kc_user_id="XXX",
        token={"access_token": "XXX", "expires_in": 60},
        access_token="XXX",
        token_expiration=datetime.utcnow() + timedelta(seconds=60),
    )
    db.session.add(user)
    db.session.commit()
    return user
