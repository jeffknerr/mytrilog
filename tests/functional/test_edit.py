
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


def test_edit_workout(client, auth, app_with_user):
    # log in
    response = auth.login(uname, pw)
    assert response.status_code == 200
    # log a workout
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
    # now make an edit (change xfit to swim)
    eurl = "mytrilog/editworkout/%s/%s 00:00:00/1" % (what, wdate)
    # 1 at end of url means this is user #1???
    response = client.post(eurl,
            data={'what': "swim", 'when': wdate,
                'amount': amt, 'weight': wgt,
                'comment': cmt},
            follow_redirects=True
            )
    assert response.status_code == 200
    bstr = "swim".encode('utf-8')
    assert bstr in response.data
    assert b"Saved your edited workout..." in response.data
    # log out the user
    response = auth.logout()
    assert response.status_code == 200
