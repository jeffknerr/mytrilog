from app.models import User, Workout

# https://testdriven.io/blog/flask-pytest/

# would be nice to define the user data somewhere once,
# so we don't have to repeat it here :(
uname = "jk"
mail = "jk@dummy.org"
pw = "FlaskIsOK"
badpw = "sdkfjlksdjfl"
wdate = "2023-01-26"
what = "xfit"
amt = 30
wgt = 160
cmt="30x40/20"

def test_new_user(new_user):
    """
    check that the username, hashed_password, and email are good
    """
    new_user.set_password(pw)
    assert new_user.email == mail
    assert new_user.check_password(pw)
    assert not new_user.check_password(badpw)
    assert new_user.username == uname
    assert new_user.get_username() == uname
    assert new_user.get_email() == mail
    u = User(username='john', email='john@example.com')
    assert u.avatar(128) != 'https://www.gravatar.com/avatar/d4c74594d841136bd6?d=identicon&s=128'
    assert u.avatar(128) == 'https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?d=identicon&s=128'

def test_new_workout(new_workout):
    """
    check that the workout details are defined correctly
    """
    assert new_workout.what == what
    assert new_workout.when == wdate
    assert new_workout.amount == amt
    assert new_workout.weight == wgt
    assert new_workout.comment == cmt
