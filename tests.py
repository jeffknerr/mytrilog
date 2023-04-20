#!/usr/bin/env python3

from datetime import datetime, timedelta
import unittest
import re
from app import create_app, db
from app.models import User, Workout
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/mytrilog/auth/login')
        self.assertTrue('Sign In' in response.get_data(as_text=True))
        self.assertTrue('New User?' in response.get_data(as_text=True))

    def test_register_login_logout(self):
        tdata = {
                'uname': "jk2756",
                'mail': "jk2756@dummy.org",
                'pw': "FlaskIsOK",
                }
        # register new account
        response = self.client.post('/mytrilog/auth/register',
                                    data={'username': tdata['uname'],
                                          'email': tdata['mail'],
                                          'password': tdata['pw'],
                                          'password2': tdata['pw'],
                                          }
                                    )
        self.assertTrue(response.status_code == 302)
        # log in with new account
        response = self.client.post('/mytrilog/auth/login',
                                    data={'username': tdata['uname'],
                                          'password': tdata['pw'],
                                          },
                                    follow_redirects=True
                                    )
        pagedata = response.get_data(as_text=True)
        sstr = "Hello,%s%s!" % ("\\s", tdata['uname'])
        self.assertTrue(re.search(sstr, pagedata))
        self.assertTrue("Log a workout?" in pagedata)
        # log out
        response = self.client.get('/mytrilog/auth/logout',
                                   follow_redirects=True
                                   )
        pagedata = response.get_data(as_text=True)
        self.assertTrue("Remember Me" in pagedata)
        self.assertTrue("New User?" in pagedata)
        self.assertTrue("Forgot Your Password?" in pagedata)
        self.assertTrue("Sign In" in pagedata)

    def test_log_workout(self):
        tdata = {
                'uname': "jk2757",
                'mail': "jk2757@dummy.org",
                'pw': "FlaskIsOKay",
                'wdate': "2023-01-26",
                'what': "xfit",
                'amt': 30,
                'wgt': 160,
                'cmt': "30x40/20",
                }
        # register new account
        response = self.client.post('/mytrilog/auth/register',
                                    data={'username': tdata['uname'],
                                          'email': tdata['mail'],
                                          'password': tdata['pw'],
                                          'password2': tdata['pw'],
                                          }
                                    )
        self.assertTrue(response.status_code == 302)
        # log in with new account
        response = self.client.post('/mytrilog/auth/login',
                                    data={'username': tdata['uname'],
                                          'password': tdata['pw'],
                                          },
                                    follow_redirects=True
                                    )
        pagedata = response.get_data(as_text=True)
        sstr = "Hello,%s%s!" % ("\\s", tdata['uname'])
        self.assertTrue(re.search(sstr, pagedata))
        self.assertTrue("Log a workout?" in pagedata)
        # log a workout
        response = self.client.post('/mytrilog/index',
                                    data={'what': tdata['what'],
                                          'when': tdata['wdate'],
                                          'amount': tdata['amt'],
                                          'weight': tdata['wgt'],
                                          'comment': tdata['cmt'],
                                          },
                                    follow_redirects=True
                                    )
        pagedata = response.get_data(as_text=True)
        sstr = "Hello,%s%s!" % ("\\s", tdata['uname'])
        self.assertTrue(re.search(sstr, pagedata))
        self.assertTrue("Logged your workout!" in pagedata)
        self.assertTrue(tdata["cmt"] in pagedata)
        self.assertTrue(tdata["what"] in pagedata)

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    def test_follow(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'susan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'john')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_workouts(self):
        # create four users
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        u3 = User(username='mary', email='mary@example.com')
        u4 = User(username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four Workouts
        now = datetime.utcnow()
        p1 = Workout(what="Run",  athlete=u1, when=now + timedelta(seconds=1))
        p2 = Workout(what="Bike", athlete=u2, when=now + timedelta(seconds=4))
        p3 = Workout(what="Swim", athlete=u3, when=now + timedelta(seconds=3))
        p4 = Workout(what="Xfit", athlete=u4, when=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        u1.follow(u2)  # john follows susan
        u1.follow(u4)  # john follows david
        u2.follow(u3)  # susan follows mary
        u3.follow(u4)  # mary follows david
        db.session.commit()

        # check the followed workouts of each user
        f1 = u1.followed_workouts().all()
        f2 = u2.followed_workouts().all()
        f3 = u3.followed_workouts().all()
        f4 = u4.followed_workouts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])


if __name__ == '__main__':
    unittest.main(verbosity=2)
