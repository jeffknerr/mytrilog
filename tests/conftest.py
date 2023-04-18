
# https://testdriven.io/blog/flask-pytest/

import pytest
from app.models import User, Workout
from sqlalchemy import delete

# import the module
from app import create_app
from app import db as _db
from app.models import User as NewUser
from config import TestingConfig
from flask import current_app

uname = "jk2756"
mail = "jk2756@dummy.org"
pw = "FlaskIsOK"
badpw = "sdkfjlksdjfl"
wdate = "2023-01-26"
what = "xfit"
amt = 30
wgt = 160
cmt = "30x40/20"


@pytest.fixture(scope="session")
def app():
    """Returns session-wide application"""

    app = create_app(TestingConfig)

    app.config.update({
        "TESTING": True,
        "SECRET_KEY": 'test',
        "BLAH": 6,
    })

    ctx = app.test_request_context()
    ctx.push()
    yield app
    ctx.pop()


@pytest.fixture(scope="session")
async def app_with_db(app):
    _db.create_all()
    yield app
    _db.session.commit()
    _db.drop_all()


@pytest.fixture()
def app_with_user(app_with_db):
    new_user = NewUser(username=uname, email=mail)
    new_user.set_password(pw)
    current_app.config["NEWVAR"] = 42
    # add the new user to the database
    _db.session.add(new_user)
    _db.session.commit()
    yield app_with_db
    _db.session.execute(delete(NewUser))
    _db.session.commit()
    _db.session.remove()


@pytest.fixture()
def client(app, app_with_db):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):

    def __init__(self, client):
        self._client = client

    def login(self, uname, pw):
        retval = self._client.post(
            '/mytrilog/auth/login',
            data={'uname': uname, 'pw': pw},
            follow_redirects=True
        )
        print("retval:", retval.status_code)
        return retval

    def logout(self):
        path = '/mytrilog/auth/logout'
        return self._client.get(path,  follow_redirects=True)


@pytest.fixture
def auth(client):
    return AuthActions(client)

# fixtures for unit tests ----------------------------


@pytest.fixture(scope='module')
def new_user():
    user = User(username=uname, email=mail)
    return user


@pytest.fixture(scope='module')
def new_workout():
    user = User(username=uname, email=mail)
    workout = Workout(what=what,
                      when=wdate,
                      amount=amt,
                      weight=wgt,
                      comment=cmt,
                      athlete=user)
    return workout


# fixtures for functional tests ---------------------

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client
