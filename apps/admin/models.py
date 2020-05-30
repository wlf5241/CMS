# encoding:utf-8
from extends import db
from werkzeug.security import generate_password_hash, check_password_hash


class Users(db.Model):
    def __init__(self, username, password, phone, email):
        self.username = username
        self.password = password
        self.phone = phone
        self.email = email

    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=True, unique=True)
    phone = db.Column(db.String(20), nullable=False, unique=True)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)
