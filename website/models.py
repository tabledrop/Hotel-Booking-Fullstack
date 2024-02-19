from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Room(db.Model):
    reservation_id = db.Column(db.Integer, primary_key=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    reservation = db.relationship('Room')
