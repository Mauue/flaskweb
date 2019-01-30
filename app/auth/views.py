import functools
import pymysql
from . import auth
from flask import  render_template, redirect, request, flash, url_for, g, session
from app.db import get_db
#from ..models import User
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import login_user,logout_user

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['Password']
        db = get_db()
        cursor = db.cursor(pymysql.cursors.DictCursor)
        error = None
        user = None

        for i in username:
            if not ((i>='0' and i<='9')or(i>='a' and i<='z')or(i>='A' and i<='Z')or(i=='_')or(i>=u'\u4e00' and i<=u'\u9fa5')):
                error = str(i)+'请输入正确的用户名。'
                break
        if error != None:
            pass
        elif not username:
            error = '请输入用户名！'
        elif not password:
            error = '请输入密码！'
        else:
            cursor.execute(
                "SELECT * FROM users WHERE user_nickname = '%s'" % (username)
            )
            user = cursor.fetchone()
            if user is None:
                error = '该用户不存在！'
            elif not check_password_hash(user['user_password'], password):
                error = '密码错误'

        if error is None:
            # login_user(user, True)
            session.clear()
            session['user_id'] = user['user_id']
            return redirect(url_for('main.index'))

        flash(error)
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['Password1']
        password2 = request.form['Password2']
        db = get_db()
        cursor = db.cursor(pymysql.cursors.DictCursor)
        error = None
        user = None
        for i in username:
            if not((i>='a' and i<='z')or(i>='A' and i<='Z')or(i>='0' and i<='9')or(i=='_')or(i>='\u4e00' and i<='\u9fa5')):
                error = '用户名有非法字符。'
                break
        for i in password:
            if not (i>='!' and i<='~'):
                error = '密码有非法字符。'
                break
        if error != None:
            pass
        elif not username:
            error = '请输入用户名！'
        elif len(username) < 2 :
            error = '用户名长度至少需要2位'
        elif len(username) > 12 :
            error = '用户名长度不能超过12'
        elif not password:
            error = '请输入密码！'
        elif len(password) < 5:
            error = '密码长度至少需要6位'
        elif len(password) > 20 :
            error = '密码长度不能超过20位'
        elif not password2:
            error = '请输入确认密码！'
        elif password != password2:
            error = '密码不一致！'
        else:

            cursor.execute(
                "SELECT * FROM users WHERE user_nickname = '%s'" % (username)
            )
            user = cursor.fetchone()
            if user is not None:
                error = '用户重名，请输入新用户！'

        if error is None:
            ip = request.remote_addr
            email ='test@mail.com'
            cursor.execute(
                "INSERT INTO users (user_nickname, user_password, user_email) VALUES ('%s','%s','%s')" %
                (pymysql.escape_string(username),pymysql.escape_string(generate_password_hash(password)),email)
            )
            cursor.execute(
                "INSERT INTO users_info (user_ip) VALUES ('%s')" %(pymysql.escape_string(ip))
            )
            db.commit()
            return redirect(url_for('.login'))
        flash(error)
    return render_template('auth/register.html')


@auth.route('/logout')
def logout():
    session.clear()
    flash('您已登出。')
    return redirect(url_for('main.index'))

#所有请求返回前 先判断登录状态
@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        cursor = get_db().cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM users WHERE user_id = '%s'" % (user_id)
        )
        g.user = cursor.fetchone()

#检测登录状态 用法：路由后加@login_required
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:

            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

