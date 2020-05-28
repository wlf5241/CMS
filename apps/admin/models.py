# encoding:utf-8
from app import db


class Users(db.Model):
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=True, unique=True)
    phone = db.Column(db.String(20), nullable=False, unique=True)