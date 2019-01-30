import pymysql
import click
from flask import current_app, g
from flask.cli import with_appcontext

#连接数据库 并返回
def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(current_app.config['SQLALCHEMY_DATABASE_HOST'],
                               current_app.config['SQLALCHEMY_DATABASE_USER'],
                               current_app.config['SQLALCHEMY_DATABASE_PAWD'],
                               current_app.config['SQLALCHEMY_DATABASE_NAME'],
                               )


    return g.db

#访问后关闭数据库？
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

#初始化数据库
def init_db():
    db = get_db()
    cursor = db.cursor()
    with current_app.open_resource('db/schema.sql') as f:
        sql = ''
        for each_line in f.readlines():
            if not each_line or each_line == '\n':
                continue
            sql += str(each_line.decode('utf8').strip())
            print(sql)
            if sql and sql[-1]==';':
                cursor.execute(sql)
                sql= ''
        db.commit()

#初始化数据库的命令 可通过输入init-db
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

#初始化app时调用
def init_app(app):
    #当app结束时调用close_db
    app.teardown_appcontext(close_db)
    #向flask添加初始化命令？
    app.cli.add_command(init_db_command)