from app.models import User, Workout

# https://testdriven.io/blog/flask-pytest/

def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check that the email, hashed_password, and email are good
    """
    uname = "jk"
    mail = "jk@dummy.org"
    pw = "FlaskIsOK"
    user = User(username=uname, email=mail)
    user.set_password(pw)
    assert user.email == mail
    assert user.check_password(pw)
    assert not user.check_password("sdjflksdjfkj")
    assert user.username == uname
    assert user.get_username() == uname
    assert user.get_email() == mail
    u = User(username='john', email='john@example.com')
    assert u.avatar(128) == 'https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?d=identicon&s=128'

def test_new_workout():
    """
    GIVEN a Workout model
    WHEN a new Workout is created
    THEN check that the email, hashed_password, and role are defined correctly
    """
    uname = "jk"
    mail = "jk@dummy.org"
    wdate = "2023-01-26"
    amt = 30
    wgt = 160
    user = User(username=uname, email=mail)
    workout = Workout(what="xfit",
                      when=wdate,
                      amount=amt,
                      weight=wgt,
                      comment="30x40/20",
                      athlete=user)
    assert workout.what == "xfit"
    assert workout.when == wdate
    assert workout.amount == amt
    assert workout.weight == wgt
