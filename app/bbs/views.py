from flask import  render_template, redirect, request, flash, url_for, g, session
from . import bbs
from ..auth.views import login_required
from app.db import get_db
import pymysql
import time
import math,bleach
from markdown import markdown
@bbs.route('/page/<int:id>')
def page(id):
    db = get_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute('''SELECT p.tid, title, text, datetime, u.username, reply,last_reply_name, last_reply_time
                      FROM topics p inner join users u on p.author_id=u.uid
                      ORDER BY last_reply_time DESC 
                      LIMIT 20 OFFSET %s'''%(20*(id-1))
    )
    posts = cursor.fetchall()

    cursor.execute('SELECT * FROM topics')
    pagenum = math.ceil(cursor.rowcount/ 20 )
    return render_template('bbs/index.html',posts = posts, pagenum = pagenum, pageid = id)

@bbs.route('/')
def index():
    return redirect(url_for('bbs.page',id=1))

@bbs.route('/new', methods = ['GET', 'POST'])
@login_required
def new():
   if request.method == 'POST':
       title = request.form['title']
       text = request.form['text']
       error = None

       if not title:
           error = "请输入标题"
       elif not text:
           error = "请输入内容"

       if not error:
           author_id = g.user['uid']
           create_time = time.strftime("%Y-%m-%d %H:%M:%S")
           db = get_db()
           cursor = db.cursor()
           cursor.execute('''INSERT INTO topics(
                        title, text, datetime, author_id,last_reply_name,last_reply_time)
                        VALUES('%s','%s','%s',%s,'%s','%s')
                    '''%(pymysql.escape_string(title),pymysql.escape_string(text),create_time,author_id,g.user['username'],create_time)
           )
           db.commit()
           return redirect(url_for('.index'))
       flash(error)
   return render_template('bbs/new.html')

def get_post(id):
    db = get_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(
        '''SELECT t.tid,title, text, datetime, reply,u.username, u.uid, u.hphoto
        FROM topics t inner join users u on t.author_id=u.uid
        WHERE t.tid = %s;'''%(id)
    )
    post = cursor.fetchone()
    return post

def get_reply(id,num):
    db = get_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(
        '''SELECT r.rid,topic_id,text, datetime,u.username, u.hphoto, floor
        FROM replys r inner join users u on r.author_id=u.uid
        WHERE topic_id = %s  ORDER BY floor LIMIT %s;'''%(id,num)

    )
    reply_list = cursor.fetchall()
    return reply_list

@bbs.route('/<int:id>',methods = ['GET','POST'])
def browse(id):
    post = get_post(id)
    if request.method == 'POST':
        if g.user is None:
            flash("请登录")
            return redirect(url_for('auth.login'))
        reply = request.form['reply']
        if not reply:
            flash("请输入回复内容")
            return redirect(url_for('bbs.browse',id=id))

        db = get_db()
        cursor = db.cursor()
        create_time = time.strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''INSERT INTO replys(
                                text, datetime, author_id, topic_id, floor)
                                VALUES('%s','%s','%s',%s,%s)
                            ''' % (pymysql.escape_string(reply), create_time, g.user['uid'], id,post['reply']+2)
                       )
        cursor.execute('UPDATE topics set reply=reply+1,last_reply_time = "%s",last_reply_name="%s"WHERE tid=%s ' % (create_time,g.user['username'],id))
        db.commit()
        return redirect(url_for('bbs.browse', id=id))

    reply_list =get_reply(id,post['reply'])
    allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                    'h1', 'h2', 'h3', 'p', 'table', 'thread', 'tr', 'th']
    post['text'] = bleach.linkify(
        bleach.clean(markdown(post['text'], output_format='html'), tags=allowed_tags, strip=True))

    if not post:
        return render_template('404.html')
    return render_template('bbs/post.html', post=post,reply_list=reply_list)

@bbs.route('/<int:id>/delete')
@login_required
def delete(id):
    post = get_post(id)
    if not post:
        return redirect(url_for('bbs.index'))
    if g.user['username']== post['username'] or g.user['permission']>=100:
        db = get_db()
        cursor = db.cursor(pymysql.cursors.DictCursor)
        cursor.execute('DELETE FROM topics WHERE tid = %s;'%(post['tid']))
        db.commit()
        return redirect(url_for('bbs.index'))
    else:
        flash('权限不足')
        return redirect(url_for('bbs.browse',id=id))