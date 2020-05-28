# encoding:utf-8
from flask import Flask
from apps.admin import bp as admin_bp  # 导入各个模块的蓝图
from apps.common import bp as common_bp
from apps.front import bp as front_bp
import config


def createApp():
    app = Flask(__name__)
    app.register_blueprint(admin_bp)  # 注册蓝图
    app.register_blueprint(common_bp)
    app.register_blueprint(front_bp)
    app.config.from_object(config)


if __name__ == '__main__':
    app = createApp()
    app.run(host="0.0.0.0", port=80, debug=True)