import os
from flask_login import UserMixin
from app import db

class Config(object):
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SECRET_KEY = os.urandom(24)
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
	

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
