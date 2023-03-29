
# https://testdriven.io/blog/flask-pytest/

import pytest
from app.models import User, Workout

uname = "jk"
mail = "jk@dummy.org"
pw = "FlaskIsOK"
badpw = "sdkfjlksdjfl"
wdate = "2023-01-26"
what = "xfit"
amt = 30
wgt = 160
cmt="30x40/20"

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

from app import create_app

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client
