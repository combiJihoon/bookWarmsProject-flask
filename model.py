from db_connect import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True,
                   nullable=False, autoincrement=True)
    user_id = db.Column(db.String(50), nullable=False, unique=True)
    user_pw = db.Column(db.String(255), nullable=False, unique=True)
    user_nickname = db.Column(db.String(20), nullable=False)
    user_email = db.Column(db.String(100), nullable=False)

    def __init__(self, user_id, user_pw, user_nickname, user_email, ):
        self.user_id = user_id
        self.user_pw = user_pw
        self.user_nickname = user_nickname
        self.user_email = user_email


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True,
                   nullable=False, autoincrement=True)
    user_id = db.Column(db.String(50), db.ForeignKey(
        'user.id'), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.Datetime, default=datetime.utcnow())

    def __init__(self, user_id, content):
        self.user_id = user_id
        self.content = content
