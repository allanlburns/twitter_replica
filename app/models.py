from app import app, db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    bio = db.Column(db.String(150))
    url = db.Column(db.String(500))
    username = db.Column(db.String(30), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(256))
    posts = db.relationship('Post', backref=db.backref('user', lazy='joined'))

    # set up methods to set and check passwords. Use password hashing!!!
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120)) # Probably shouldn't be unique to allow multiple messages from same person/email.
    message = db.Column(db.String(1000))

class Post(db.Model):
    # attributes corrolate to columns
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tweet = db.Column(db.String(140))
    date_posted = db.Column(db.DateTime, default=datetime.now())

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
