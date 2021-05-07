from flask_wtf import FlaskForm, RecaptchaField
#下面RegisterForm继承的就是上面import 引入的是FlaskForm类

from flask_wtf.file import FileField, FileRequired, FileAllowed
#文件上传类表单

from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError

#但是验证的任务交给 wtforms,要提一下的是,Email验证报错的话,是pip install wtforms版本太高,
#解决方法有两个
# 第一个方法 :安装低版本,百度一下哪一个合适.
# 第二个方法 : 单独 pip install email-validator, 也就是另安装 email-validator
from app.models import User


#注册表单
class RegisterForm(FlaskForm):
    #验证网页端post提交过来的Username, Password, Reapeat Password, Email, 也就是用户名,密码,二次密码,邮箱,最后还有验证提交注册
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=30)])
    confirm = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    recaptcha = RecaptchaField()
    submit = SubmitField('注册')

    #从db数据库User里查询 是否存在同名用户,返回用户已存在
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('用户名已存在')

    # 从db数据库User里查询 是否存在同名邮箱,返回邮箱已存在
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('邮箱已存在')

#登陆表单
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=20)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=30)])
    remember = BooleanField('Rememberme')  #保留token
    recaptcha = RecaptchaField()
    submit = SubmitField('登陆')

#提交重置密码需求
class ResetPasswordRequest(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('发送')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if not email:
            raise ValidationError('邮箱不存在')


#重置密码表单

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=30)])
    confirm = PasswordField('Repeat Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('确定')

class Texts(FlaskForm):
    text = TextAreaField('留言板', validators=[DataRequired(), Length(min=3, max=400)])
    submit = SubmitField('提交')

class UploadFile(FlaskForm):
    photo = FileField('image', validators=[FileRequired(), FileAllowed(['png', 'jpg', 'jpeg', 'gif'], 'Images only!')])
    submit = SubmitField('提交')