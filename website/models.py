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
    runs = db.relationship('Run')
    lifts = db.relationship('Lift')
    foods = db.relationship('Food')

    def get_id(self):
        return (self.user_id)


class Run(db.Model):
    running_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    running_cals = db.Column(db.Integer)
    datetime = db.Column(db.DateTime(timezone=True), default=func.now())


class Lift(db.Model):
    lift_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    lifting_cals = db.Column(db.Integer)
    datetime = db.Column(db.DateTime(timezone=True), default=func.now())


class Food(db.Model):
    food_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    food_item = db.Column(db.String(150))
    cals_eaten = db.Column(db.Integer)
    datetime = db.Column(db.DateTime(timezone=True), default=func.now())
