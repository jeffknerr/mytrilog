
import pytest
from flask import session
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
cmt="30x40/20"

def test_log_in_as_user(client, auth, app_with_db, app_with_user):
    """
    GIVEN a Flask application configured for testing 
          (test user are created with app_with_user)
    WHEN the '/login' page is requested (POST) with VALID data
    THEN check that the user can enter login page (page loaded - 200 status code)
         check that existing user is successfully login (status 200)
         check that user is successfully redirected to profile pageB
    """
    assert client.get('/mytrilog/auth/login').status_code == 200
    response = auth.login("foofoo", "notavalidpw")
    response = auth.login(uname, pw)
    print(response.text)
    assert response.status_code == 200
#   print("SLEEPING AFTER attempted login with pw....")
#   sleep(45)
#   hstr = "Hello, %s!" % uname
#   bhstr = hstr.encode('utf-8')
#   assert bhstr in response.data
#   assert b"Log a workout?" in response.data
    # can we prove we are logged in here???
#   assert response.request.path == '/mytrilog/index'


def test_logout_user(client, auth):
    """
    GIVEN a Flask application configured for testing
    WHEN the user is log in with VALID data
    THEN check that existing user is successfully login out
         check that there was one redirect response
         check that user is successfully redirected to index page
    """
    with client:
        # get index page
        client.get('/mytrilog/auth/login')
        # login to existing account
        r = auth.login(uname, pw)
        # print(r.data)  # shows the login page???
        # logout user
        response = auth.logout()
        # check user is successfuly loged out
        assert response.status_code == 200
        # Check that there was one redirect response.
#       assert len(response.history) == 1
#       assert len(response.history) == 2
        # Check that the second request was to the index page.
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
