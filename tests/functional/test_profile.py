
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


def test_edit_profile(client, auth, app_with_user):
    # try without logging in first...
    cget = client.get('/mytrilog/edit_profile')
    assert cget.status_code == 302
    assert b"Redirecting" in cget.data
    # log in
    response = auth.login(uname, pw)
    assert response.status_code == 200
    # try again after logging in
    cget = client.get('/mytrilog/edit_profile')
    assert cget.status_code == 200
    response = client.post("/mytrilog/edit_profile",
            data={'username': "JK", 
                  'about_me': "JustKidding",
                 },
            follow_redirects=True
            )
    assert response.status_code == 200
    hstr = "Edit Profile"
    bhstr = hstr.encode('utf-8')
    assert bhstr in response.data
    bstr = "Your changes have been saved.".encode('utf-8')
    assert bstr in response.data
    # go back to user page and make sure text is there
    cget = client.get('/mytrilog/edit_profile')
    assert cget.status_code == 200
    assert b"JustKidding" in cget.data
    # log out the user
    response = auth.logout()
    assert response.status_code == 200
