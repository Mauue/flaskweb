from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    user = StringField('用户名', validators=[Required()])
    password = StringField('密码', validators=[Required()])
    submit = SubmitField('登陆')

class RegisterForm(FlaskForm):
    user = StringField('用户名', validators=[Required()])
    password = StringField('密码', validators=[Required()])
    password2 = StringField('密码', validators=[Required()])
    submit = SubmitField('完成注册')