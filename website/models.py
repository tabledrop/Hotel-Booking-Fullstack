from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Room(db.Model):
    reservation_id = db.Column(db.Integer, primary_key=True)
    checkin = db.Column(db.DateTime(timezone=True), default=func.now())
    reservation_len = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    reservation = db.relationship('Room')
