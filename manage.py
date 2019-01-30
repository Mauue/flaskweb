import os
from app import create_app
#from app.models import User, Post
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

#创建应用
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)
# 加载数据库
# def make_shell_context():
#     return dict(app=app, db=db, User=User, Post=Post)
# manager.add_command("shell", Shell(make_context=make_shell_context()))
# manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

#pbkdf2:sha256:50000$5UUSM8WK$a9f42748d0a4d34808d4335d951ba413d734a59789919f76640d5ef32d5b47d2
