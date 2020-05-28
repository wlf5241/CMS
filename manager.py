# encoding:utf-8
from flask_script import Manager
from app import createApp
from apps.admin import models as admin_models

app = createApp()
manager = Manager(app)


@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
@manager.option('-t', '--phone', dest='phone')
def create_user(username, password, phone, email):
    user = admin_models.Users(username=username, password=password, phone=phone, email=email)
    print(f'添加用户成功：{user.id}')


if __name__ == '__main__':
    manager.run()
