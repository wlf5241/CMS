# encoding:utf-8
from flask import Blueprint, render_template, request, session, redirect, url_for, make_response
from io import BytesIO
from datetime import timedelta
import config
from .models import Users
from .forms import LoginForm
from .decorators import login_require
from utils.captcha import create_validate_code

bp = Blueprint("admin", __name__)


@bp.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if session.get('image'):  # 回退未获取验证码……
            if session.get('image').lower() != form.captcha.data.lower():
                return render_template('admin/login.html', form=form, message='验证码错误！')
            user = Users.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                session[config.ADMIN_USER_ID] = user.uid
                if request.form.get('online'):  # 选择了记录登陆状态
                    session.permanent = True
                    bp.permanent_session_lifetime = timedelta(days=30)  # 有效期30天
                return redirect(url_for('admin.index'))
            else:
                return render_template('admin/login.html', form=form, message='用户名或密码错误！')
        else:
            return render_template('admin/login.html', form=form, message='请刷新验证码！')
    else:
        return render_template('admin/login.html', form=form)


@bp.route('/logout/')
@login_require
def logout():
    del session[config.ADMIN_USER_ID]
    return redirect(url_for('admin.login'))


@bp.route('/code/')
def get_code():
    code_img, strs = create_validate_code()
    buf = BytesIO()
    code_img.save(buf, 'JPEG', quality=70)
    response = make_response(buf.getvalue())
    response.headers['Content-Type'] = 'image/jpeg'
    session['image'] = strs
    return response


@bp.route('/')
@login_require
def index():
    return render_template('admin/index.html')
