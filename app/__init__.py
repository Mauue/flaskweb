from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
# from flask_sqlalchemy import SQLAlchemy

from config import config
from flask_pagedown import PageDown
import os

bootstrap = Bootstrap()

#富文本编辑器
pagedown = PageDown()

def create_app(config_name='default'):

    app = Flask(__name__,instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'app.db'),
    )


    #加载配置文件
    if config_name == 'default':
        app.config.from_object(config[config_name])
        config[config_name].init_app(app)
        # load the instance config, if it exists, when not testing
    else:
        # load the test config if passed in
        app.config.from_mapping(config_name)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #CSS
    bootstrap.init_app(app)
    #数据库初始化
    from app import db
    db.init_app(app)
    #登陆系统初始化
    # login_manager.init_app(app)
    #富文本编辑器初始化
    pagedown.__init__(app)

    # 附加路由和自定义的错误页面
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')
    # from .bbs import bbs as bbs_blueprint
    # app.register_blueprint(bbs_blueprint, url_prefix='/bbs')
    from .blog import blog as blog_blueprint
    app.register_blueprint(blog_blueprint, url_prefix='/blog')
    from .movie import movie as movie_blueprint
    app.register_blueprint(movie_blueprint, url_prefix='/movie')

    return app