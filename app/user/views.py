from flask import  render_template, redirect, request, flash, url_for, g, session,Flask,Request
from . import user
from ..auth.views import login_required
from ..db import get_db
import time,os
@user.route('/')
@login_required
def index():
    return render_template('user/index.html',user=g.user)

@user.route('/avatar',methods=['GET','POST'])
@login_required
def avatar():
    flash("图片大小不能超过1MB，上传后可能出现连接错误等问题")
    if request.method == 'POST':

        try:
            avatar_file = request.files['avatar']
        except:
            flash('请选择文件')
            return redirect(url_for('user.avatar'))

        # if size > 1000000:
        #     flash('文件不能超过1MB')
        #     return redirect(url_for('user.avatar'))
        fname = avatar_file.filename
        ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
        flag = fname.rsplit('.', 1)[1]
        if not (flag in ALLOWED_EXTENSIONS):
            flash('文件类型出错')
            return redirect(url_for('user.avatar'))
        if g.user['user_photo']:
            try:
                os.remove('app/static/avatar/%s.%s'%(g.user['user_nickname'],g.user['user_photo'].split('?', 1)[0]))
            except IndexError:
                os.remove('app/static/avatar/%s.%s' % (g.user['user_nickname'], g.user['user_photo']))
            except:
                pass
        avatar_file.save('{}{}.{}'.format('app/static/avatar/',g.user['user_nickname'],flag))
        db=get_db()
        cursor=db.cursor()
        cursor.execute('UPDATE users set user_photo="%s" WHERE user_id=%s '%(g.user['user_nickname']+'.'+flag+'?v='+time.strftime("%y%m%d%H%M%S", time.localtime()),g.user['user_id']))
        db.commit()
        flash('已更新头像')
        return redirect(url_for('user.index'))
    return render_template('user/avatar.html',user=g.user)