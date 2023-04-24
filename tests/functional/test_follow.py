
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


def test_follow_user(client, auth, app_with_user):
    # register one user
    u1 = "Abby"
    e1 = "abby@example.com"
    p1 = "ruffruffbarkbark"
    response = client.post("/mytrilog/auth/register",
            data={'username': u1, 'email': e1,
                'password': p1, 'password2': p1},
            follow_redirects=True
            )
    assert response.status_code == 200
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
    # go to first user's profile page
    response = client.get("/mytrilog/user/%s" % (u1))
    assert response.status_code == 200
    # now follows the first user
    response = client.get("/mytrilog/follow/%s" % (u1), 
                          follow_redirects=True)
    assert response.status_code == 200
    hstr = "You are following %s!" % u1
    bhstr = hstr.encode('utf-8')
    assert bhstr in response.data
    hstr = "User: %s" % u1
    bhstr = hstr.encode('utf-8')
    assert bhstr in response.data
    assert b"Last seen on" in response.data
    assert b"1 followers, 0 following." in response.data
    # now unfollows the first user
    response = client.get("/mytrilog/unfollow/%s" % (u1), 
                          follow_redirects=True)
    assert response.status_code == 200
    hstr = "You are not following %s." % u1
    bhstr = hstr.encode('utf-8')
    assert bhstr in response.data
    hstr = "User: %s" % u1
    bhstr = hstr.encode('utf-8')
    assert bhstr in response.data
    assert b"Last seen on" in response.data
    assert b"0 followers, 0 following." in response.data
    # can not follows yourself
    response = client.get("/mytrilog/follow/%s" % (u2), 
                          follow_redirects=True)
    assert response.status_code == 200
    hstr = "You cannot follow yourself!"
    bhstr = hstr.encode('utf-8')
    assert bhstr in response.data
    # log out the user
    response = auth.logout()
    assert response.status_code == 200
