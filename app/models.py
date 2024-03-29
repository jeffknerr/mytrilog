
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db,login
from hashlib import md5
from time import time
import jwt

# add the self-referential followers relationship
# no class, since it's just an auxiliary table (with just foreign keys)
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    workouts = db.relationship('Workout', backref='athlete', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship('User', secondary=followers,
                               primaryjoin=(followers.c.follower_id==id),
                               secondaryjoin=(followers.c.followed_id==id),
                               backref=db.backref('followers',lazy='dynamic'), 
                               lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_workouts(self):
        followed = Workout.query.join(
            followers, (followers.c.followed_id == Workout.who)).filter(
                followers.c.follower_id == self.id)
        own = Workout.query.filter_by(who=self.id)
        return followed.union(own).order_by(Workout.when.desc())

    def get_reset_password_token(self, expires_in=300):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return db.session.get(User, int(id))


class Workout(db.Model):
    """workout objects, unique in what and when"""
    id = db.Column(db.Integer, primary_key=True)
    what = db.Column(db.String(128))
    when = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    amount = db.Column(db.Float, default=0)
    weight = db.Column(db.Float)
    who = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment = db.Column(db.String(40))

    def __repr__(self):
        return '<Workout {} {} {}>'.format(self.what,self.amount,self.when)    

    def getUsername(self):
        u = db.session.get(User, self.who)
        return u.username

    def getDOM(self):
        """get day of month"""
        return int(self.when.strftime("%d"))
    def getDOY(self):
        """get day of year"""
        return int(self.when.strftime("%j"))
    def getWhen(self):
        return self.when
    def getDate(self):
        return self.when
    def getMonthName(self): 
        return self.when.strftime("%B")
    def getComment(self):
        return self.comment
    def getWeight(self):
        return self.weight


@login.user_loader
def load_user(id):
      return db.session.get(User, int(id))
