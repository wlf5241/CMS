# encoding:utf-8
from flask import Blueprint, render_template, request, session, redirect, url_for, make_response, jsonify
from io import BytesIO
from datetime import timedelta
from xpinyin import Pinyin
import config
from .models import Users
from .forms import LoginForm, ProductCatForm
from .decorators import login_require
from .utils import GetUser, BuildTree, BuildTable, BuildCatList
from apps.common.models import ProductCatagory
from utils.captcha import create_validate_code
from extends import db

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
            return render_template('admin/login.html', form=form, message='验证码已失效！')
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


@bp.route('/profile')
@login_require
def profile():
    return render_template('admin/profile.html', user=GetUser())


@bp.route('/checkpwd/')
@login_require
def checkpwd():
    oldpwd = request.args.get('oldpwd', '')
    user = GetUser()
    if user is not None and user.check_password(oldpwd):
        data = {
            "name": user.email,
            "status": 11
        }
    else:
        data = {
            'name': None,
            'status': 00
        }
    return jsonify(data)


@bp.route('/EditPassword', methods=['GET', 'POST'])
@login_require
def editpwd():
    if request.method == 'GET':
        return render_template('admin/edit_pwd.html')
    else:
        GetUser().password = request.form.get('newpwd1')
        db.session.commit()
        return render_template('admin/edit_pwd.html', message='密码修改成功!')


@bp.route('/AddProductCatagory', methods=['GET', 'POST'])
@login_require
def product_cat_add():
    if request.method == 'GET':
        categorys = ProductCatagory.query.all()
        ls = [{'sid': x.self_id, 'pid': x.parent_id, 'tname': x.type_name} for x in categorys]
        html = BuildTable(BuildTree(ls, 0, 0))
        return render_template('admin/product_cat_add.html', body=html)
    else:
        form = ProductCatForm(request.form)
        if form.validate():
            tname = request.form.get('type_name')
            dirpath = request.form.get('dirpath')
            check = request.form.get('check')
            if check or dirpath is None:
                dirpath = Pinyin().get_pinyin(tname, '')
            pid = request.form.get('parent_id')
            kws = request.form.get('keywords')
            des = request.form.get('description')
            psort = request.form.get('product_sort')
            vis = request.form.get('visable')
            insert = ProductCatagory(parent_id=pid, type_name=tname, keywords=kws, description=des, product_sort=psort,
                                     visable=vis, dirPath=dirpath)
            db.session.add(insert)
            db.session.commit()
            return redirect(url_for('admin.product_cat_list'))
        else:
            return "输入有误，校验未通过"


@bp.route('/ProductCatagoryList/', methods=['GET'])
@login_require
def product_cat_list():
    if request.method == 'GET':
        categorys = ProductCatagory.query.all()
        ls = [{'sid': x.self_id, 'pid': x.parent_id, 'tname': x.type_name, 'psort': x.product_sort,
               'description': x.description, 'dirpath': x.dirPath} for x in categorys]
        html = BuildCatList(BuildTree(ls, 0, 0))
        return render_template('admin/product_cat_list.html', body=html)


@bp.route('/EditProductCatagory/<id>/', methods=['GET', 'POST'])
@login_require
def product_cat_edit(id):
    if request.method == 'GET':
        current = ProductCatagory.query.filter_by(self_id=id).first()
        categorys = ProductCatagory.query.all()  # 取得所有分类
        ls = [{'sid': x.self_id, 'pid': x.parent_id, 'tname': x.type_name} for x in categorys]
        html = BuildTable(BuildTree(ls, 0, 0))
        return render_template('admin/product_cat_edit.html', content=current, body=html)
    else:
        form = ProductCatForm(request.form)
        if form.validate():
            tname = request.form.get('type_name')
            dirpath = request.form.get('dirpath')
            check = request.form.get('check')
            sid = int(request.form.get('self_id'))
            if check or dirpath is None:
                dirpath = Pinyin().get_pinyin(tname, '')
            pid = request.form.get('parent_id')
            kws = request.form.get('keywords')
            des = request.form.get('description')
            psort = request.form.get('product_sort')
            vis = request.form.get('visable')
            ProductCatagory.query.filter(ProductCatagory.self_id == sid).update(
                {ProductCatagory.parent_id: pid, ProductCatagory.type_name: tname, ProductCatagory.dirPath: dirpath,
                 ProductCatagory.keywords: kws, ProductCatagory.description: des,
                 ProductCatagory.product_sort: psort, ProductCatagory.visable: vis
                 })
            db.session.commit()
            return redirect(url_for('admin.product_cat_list'))


@bp.route('/DelProductCatagory/<id>', methods=['GET'])
@login_require
def product_cat_del(id):
    cat1 = ProductCatagory.query.filter(ProductCatagory.self_id == id).first()  # 查询出数据库中的记录
    db.session.delete(cat1)
    db.session.commit()
    return redirect(url_for('admin.product_cat_list'))


@bp.route('/welcome/')
@login_require
def welcome():
    return render_template('admin/welcome.html')


@bp.route('/')
@login_require
def index():
    return render_template('admin/index.html')
