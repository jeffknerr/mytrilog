
import pytest
from flask import session
from flask import current_app
from sqlalchemy import select
from app.models import User
from time import sleep

uname = "jk2756"
mail = "jk2756@dummy.org"
pw = "FlaskIsOK"
badpw = "sdkfjlksdjfl"
wdate = "2023-01-26"
what = "xfit"
amt = 30
wgt = 160
cmt = "30x40/20"


def test_log_in_as_user(client, auth, app_with_user):
    """
    GIVEN a Flask application configured for testing
          (test user are created with app_with_user)
    WHEN the '/login' page is requested (POST) with VALID data
    THEN check that the user can enter login page
         check that existing user is successfully logged in
         check that user is successfully redirected to profile page
    """
    # check main login page
    cget = client.get('/mytrilog/auth/login')
    assert cget.status_code == 200
    # check invalid user login
    response = auth.login("foofoo", "notavalidpw")
    assert b"Sign In" in response.data
    # check valid user login
    response = auth.login(uname, pw)
    assert response.status_code == 200
    hstr = "Hello, %s!" % uname
    bhstr = hstr.encode('utf-8')
    assert bhstr in response.data
    assert b"Log a workout?" in response.data
    assert b"Sign In" not in response.data


def test_logout_user(client, auth, app_with_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the user is log in with VALID data
    THEN check that existing user is successfully login out
         check that there was one redirect response
         check that user is successfully redirected to index page
    """
    # first log in
    response = auth.login(uname, pw)
    assert response.status_code == 200
    hstr = "Hello, %s!" % uname
    bhstr = hstr.encode('utf-8')
    assert bhstr in response.data
    assert b"Log a workout?" in response.data
    assert b"Sign In" not in response.data
    # now log out
    response = auth.logout()
    assert response.status_code == 200
    # should go straight to /mytrilog/auth/login
    assert len(response.history) == 1
#   print(response.history[0].data)
    assert response.request.path == "/mytrilog/auth/login"


# https://testdriven.io/blog/flask-pytest/

def test_login_page(test_client):
    """look for certain strings and valid status in login page"""
    response = test_client.get('/mytrilog/auth/login')
    assert response.status_code == 200
    assert b"Sign In" in response.data
    assert b"Username" in response.data
    assert b"Password" in response.data
    assert b"Remember Me" in response.data
    assert b"New User?" in response.data
    assert b"Forgot Your Password?" in response.data


def test_redir_to_login(test_client):
    """look for redirect to login page"""
    response = test_client.get('/mytrilog/')
    assert response.status_code == 302
    assert b"You should be redirected automatically" in response.data
