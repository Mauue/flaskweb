#路由
from datetime import datetime
from flask import render_template, session, redirect, url_for, flash,g,current_app,request
from .import movie
from ..db import get_db
from .spider import create_database,C_Thread,start
import time,pymysql
from math import ceil
from threading import Thread,Lock
import json
from .tool import set_conditions

@movie.route('/', methods=['GET', 'POST'])
def index():

    return render_template('movie/index.html')


@movie.route('/search',methods=['POST'])
def search():
    search_condition = set_conditions(request.form.to_dict())
    db = get_db()
    cursor=db.cursor()
    cursor.execute(
        'SELECT COUNT(*) FROM movies %s' % (search_condition.strip())
    )
    num = cursor.fetchone()
    cursor.execute(
        'SELECT movie_name,movie_transname,movie_dbscore,movie_imdbscore '
        'FROM movies %s LIMIT 20 OFFSET %s'%
        (search_condition.strip(),(int(request.form["page"])-1)*20)
    )
    movies = cursor.fetchall()

    return json.dumps([num,movies])


@movie.route('/create')
def create():
    if g.user is None or g.user['user_permission'] <=200 :
        flash('权限不足')
        return redirect(url_for('movie.index'))
    try:
        create_database()
        flash('数据库创建成功','success')
    except:
        flash('数据库创建失败','danger')
    return redirect(url_for('movie.index'))


@movie.route('/initialize')
def delete():
    if g.user is None or g.user['user_permission'] <=200 :
        flash('权限不足')
        return redirect(url_for('movie.index'))
    try:
        create_database(delete_old=True)
        flash('数据库初始化成功','success')
    except:
        flash('数据库初始化失败','danger')
    return redirect(url_for('movie.index'))



@movie.route('/update')
def update():
    if g.user is None or g.user['user_permission'] <=200 :
        flash('权限不足')
        return redirect(url_for('movie.index'))
    # db = pymysql.connect(current_app.config['SQLALCHEMY_DATABASE_HOST'],
    #                      current_app.config['SQLALCHEMY_DATABASE_USER'],
    #                      current_app.config['SQLALCHEMY_DATABASE_PAWD'],
    #                      current_app.config['SQLALCHEMY_DATABASE_NAME'],
    #                      )
    # th = Thread(target=spider.main,args=[db])

    # txtLock = Lock()
    start('https://www.dytt8.net/html/gndy/jddy/list_63_')
    # thread1 = C_Thread(1, 'https://www.dytt8.net/html/gndy/dyzz/list_23_', txtLock)
    # thread2 = C_Thread(2, 'https://www.dytt8.net/html/gndy/jddy/list_63_', txtLock)
    # thread1.start()
    # thread2.start()
    return redirect(url_for('movie.index'))



