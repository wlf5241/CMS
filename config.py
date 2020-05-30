#encoding:utf-8
import os
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:yjm1062@127.0.0.1:3306/defaultDB'
SQLALCHEMY_TRACK_MODIFICATIONS = False  # 动态追踪修改设置
SQLALCHEMY_ECHO = True  # 查询时显示原始语句
SECRET_KEY = os.urandom(24)
CSRF_ENABLED = True
ADMIN_USER_ID = 'ADMINYJM'