
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
wdate = "2024-07-25"
what = "xfit"
amt = 30
wgt = 160
cmt = "30x40/20"


def test_log_in_as_user(client, auth, app_with_user):
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
    # now log out
    response = auth.logout()


def test_logout_user(client, auth, app_with_user):
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
    # should go straight to /mytrilog/auth/login, so only 1 item in list
    assert len(response.history) == 1
#   print(response.history[0].data)
    assert response.request.path == "/mytrilog/auth/login"

def test_about(client, auth, app_with_user):
    # first log in
    response = auth.login(uname, pw)
    assert response.status_code == 200
    hstr = "Hello, %s!" % uname
    bhstr = hstr.encode('utf-8')
    assert bhstr in response.data
    # now go to About page
    response = client.get("/mytrilog/about")
    assert response.status_code == 200
    bstr = "This is the start of".encode('utf-8')
    assert bstr in response.data
    bstr = "Jeff's triathlon training log app".encode('utf-8')
    assert bstr in response.data
    # now log out
    response = auth.logout()

def test_profile(client, auth, app_with_user):
    # first log in
    response = auth.login(uname, pw)
    assert response.status_code == 200
    hstr = "Hello, %s!" % uname
    bhstr = hstr.encode('utf-8')
    assert bhstr in response.data
    # now go to Profile page
    response = client.get("/mytrilog/user/%s" % uname)
    assert response.status_code == 200
    ustr = "User: %s" % uname
    bstr = ustr.encode('utf-8')
    assert bstr in response.data
    bstr = "Last seen on:".encode('utf-8')
    assert bstr in response.data
    bstr = "Edit your profile".encode('utf-8')
    assert bstr in response.data
    # try one that doesn't exist
    response = client.get("/mytrilog/user/sdkjfsjflkj")
    assert response.status_code == 404
    # now log out
    response = auth.logout()

def test_stats(client, auth, app_with_user):
    # first log in
    response = auth.login(uname, pw)
    assert response.status_code == 200
    hstr = "Hello, %s!" % uname
    bhstr = hstr.encode('utf-8')
    assert bhstr in response.data
    # now go to Stats page
    response = client.get("/mytrilog/stats")
    assert response.status_code == 200
    bstr = "Your Statistics".encode('utf-8')
    assert bstr in response.data
    bstr = "for the last 30 days of data...".encode('utf-8')
    assert bstr in response.data
    # now log out
    response = auth.logout()

def test_ytd(client, auth, app_with_user):
    # first log in
    response = auth.login(uname, pw)
    assert response.status_code == 200
    hstr = "Hello, %s!" % uname
    bhstr = hstr.encode('utf-8')
    assert bhstr in response.data
    # now go to YTD page
    response = client.get("/mytrilog/ytd")
    assert response.status_code == 200
    bstr = "your year-to-date data...".encode('utf-8')
    assert bstr in response.data
    # now log out
    response = auth.logout()

def test_plots(client, auth, app_with_user):
    # first log in
    response = auth.login(uname, pw)
    assert response.status_code == 200
    hstr = "Hello, %s!" % uname
    bhstr = hstr.encode('utf-8')
    assert bhstr in response.data
    # now go to plot pages (should work/be ok)
    response = client.get("/mytrilog/plot/%s" % uname)
    assert response.status_code == 200
    response = client.get("/mytrilog/ytdplot/%s" % uname)
    assert response.status_code == 200
    # try non-existent ones (if logged in, should redit to user/uname)
    response = client.get("/mytrilog/plot/%s" % uname+"sdfsdfdf")
    assert response.status_code == 302
    response = client.get("/mytrilog/ytdplot/%s" % uname+"sdfsdfdf")
    assert response.status_code == 302
    # now log out
    response = auth.logout()

def test_unloggedin_user(client, auth, app_with_user):
    # since we have app_with_user as param, should have a valid
    # but non-logged in user already, and all of these should
    # just redirect back to login page
    response = client.get("/mytrilog/plot/%s" % uname)
    assert response.status_code == 302
    response = client.get("/mytrilog/ytdplot/%s" % uname)
    assert response.status_code == 302
    response = client.get("/mytrilog/user/%s" % uname)
    assert response.status_code == 302
    response = client.get("/mytrilog/ytd")
    assert response.status_code == 302
    response = client.get("/mytrilog/edit")
    assert response.status_code == 302
    response = client.get("/mytrilog/explore")
    assert response.status_code == 302

def test_log_a_workout(client, auth, app_with_user):
    # valid user login
    response = auth.login(uname, pw)
    assert response.status_code == 200
    hstr = "Hello, %s!" % uname
    bhstr = hstr.encode('utf-8')
    assert bhstr in response.data
    # now add a workout
    response = client.post("/mytrilog/index",
            data={'what': what, 'when': wdate,
                'amount': amt, 'weight': wgt,
                'comment': cmt},
            follow_redirects=True
            )
    assert response.status_code == 200
    hstr = "Hello, %s!" % uname
    bhstr = hstr.encode('utf-8')
    assert bhstr in response.data
    bstr = "Logged your workout!".encode('utf-8')
    assert bstr in response.data
    bstr = what.encode('utf-8')
    assert bstr in response.data
    bstr = cmt.encode('utf-8')
    assert bstr in response.data
    # now log out
    response = auth.logout()

def test_explore(client, auth, app_with_user):
    # valid user login
    response = auth.login(uname, pw)
    assert response.status_code == 200
    hstr = "Hello, %s!" % uname
    bhstr = hstr.encode('utf-8')
    assert bhstr in response.data
    # now add a workout
    response = client.post("/mytrilog/index",
            data={'what': what, 'when': wdate,
                'amount': amt, 'weight': wgt,
                'comment': cmt},
            follow_redirects=True
            )
    assert response.status_code == 200
    hstr = "Hello, %s!" % uname
    bhstr = hstr.encode('utf-8')
    assert bhstr in response.data
    bstr = "Logged your workout!".encode('utf-8')
    assert bstr in response.data
    bstr = what.encode('utf-8')
    assert bstr in response.data
    bstr = cmt.encode('utf-8')
    assert bstr in response.data
    # now log out
    response = auth.logout()
    # register another user
    u2 = "Lily"
    e2 = "lily@example.com"
    p2 = "woofwoofbarkbark"
    response = client.post("/mytrilog/auth/register",
            data={'username': u2, 'email': e2,
                'password': p2, 'password2': p2},
            follow_redirects=True
            )
    assert response.status_code == 200
    # log them in
    response = auth.login(u2, p2)
    assert response.status_code == 200
    # go to explore
    response = client.get("/mytrilog/explore")
    assert response.status_code == 200
    # should be able to see first user's workout
    bstr = what.encode('utf-8')
    assert bstr in response.data
    bstr = cmt.encode('utf-8')
    assert bstr in response.data
    bstr = uname.encode('utf-8')
    assert bstr in response.data
    # now log out
    response = auth.logout()

# -------------------------------------------
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
