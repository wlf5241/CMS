# encoding:utf-8
from flask import Blueprint

bp = Blueprint("front", __name__)


@bp.route("/")  # 前台访问不需要前缀
def index():
    return "这是前台首页"
