from time import timezone
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(100))
    mile = db.Column(db.Float)
    five_k = db.Column(db.Float)
    bench = db.Column(db.Integer)
    squat = db.Column(db.Integer)
    deadlift = db.Column(db.Integer)
    calories = db.Column(db.Float)

    def get_id(self):
        return (self.user_id)
