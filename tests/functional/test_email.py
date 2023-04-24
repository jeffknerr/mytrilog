
import pytest
from flask import session
from flask import current_app
from sqlalchemy import select
from app.models import User
from time import sleep


uname = "jk2756"
mail = "jk2756@dummy.org"
pw = "FlaskIsOK"

def test_email(client, auth, app_with_user):
    # should not do anything with a non-registered user
    response = client.post("/mytrilog/auth/reset_password_request",
            data={'email': "dummyemail@nonexistent.org"},
            follow_redirects=True
            )
    assert response.status_code == 200
    assert b"Check your email for the instructions to reset" in response.data
