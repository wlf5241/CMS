# encoding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email


class LoginForm(FlaskForm):
    username = StringField(label='用户名', validators=[InputRequired('用户名为必填项'), Length(3, 20, '用户名长度3-20')],
                           render_kw={'placeholder': '用户名', 'class': 'input-text size-L'})
    password = PasswordField(label='密码', validators=[InputRequired('密码为必填项'), Length(6, 18, '密码长度6-18')],
                             render_kw={'placeholder': '密码', 'class': 'input-text size-L'})
    captcha = StringField(label='验证码', validators=[InputRequired('验证码为必填项'), Length(4, 4, '验证码长度为4位')],
                          render_kw={'placeholder': '验证码', 'class': 'input-text size-L', 'style': "width:150px;"})
