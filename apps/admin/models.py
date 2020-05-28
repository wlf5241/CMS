# encoding:utf-8
from sqlobject import *
import re


class Users(SQLObject):
    username = StringCol(length=50, notNone=True)
    password = StringCol(length=100, notNone=True)
    email = StringCol(length=100, unique=True)
    phone = IntCol(length=11, unique=True, notNone=True)


Users.createTable()
