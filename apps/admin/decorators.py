# encoding:utf-8
from functools import wraps
from flask import session, redirect, url_for


def login_require(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('admin.login'))

    return wrapper
