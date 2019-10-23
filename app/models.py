from app import app, db
from datetime import datetime



class Post(db.Model):
    # attributes corrolate to columns
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    tweet = db.Column(db.String(140))
    date_posted = db.Column(db.DateTime, default=datetime.now())
