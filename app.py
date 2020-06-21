# encoding:utf-8
from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from apps.admin import bp as admin_bp  # 导入各个模块的蓝图
from apps.common import bp as common_bp
from apps.front import bp as front_bp
from extends import db
import config

csrf = CSRFProtect()


def createApp():
    app = Flask(__name__)
    app.register_blueprint(admin_bp)  # 注册蓝图
    app.register_blueprint(common_bp)
    app.register_blueprint(front_bp)
    app.config.from_object(config)
    return app


if __name__ == '__main__':
    app = createApp()
    db.init_app(app)
    csrf.init_app(app)
    app.run(host="0.0.0.0", port=80, debug=True)
