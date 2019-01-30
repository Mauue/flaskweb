#模板
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    post = db.relationship('Post', backref='user')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verifu_password(self, password):
        return check_password_hash(self.password_hash, password)
    # 测试时用
    def __repr__(self):
        return '<User %r>' % self.username

class Post(db.Model):
    __tablename__ = 'posts'
    pid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'))
    post_time = db.Column(db.DateTime)
    post_title = db.Column(db.String(64), index=True)
    post_text = db.Column(db.Text)
    #帖子类型
    post_type = db.Column(db.SmallInteger, default=0)
    #测试时用
    def __repr__(self):
        return '<Post %r>' % self.post_title

#加载回调函数
from . import login_manager
@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))