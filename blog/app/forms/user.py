from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
# 用户注册表单
from app.extensions import photos
from app.models import User


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[Length(4, 20, message='用户名必须在4~20个字符之间')])
    password = PasswordField('密码', validators=[Length(6, 20, message='密码长度必须在6~20个字符之间')])
    confirm = PasswordField('确认密码', validators=[EqualTo('password', message='两次密码不一致')])
    email = StringField('邮箱', validators=[Email(message='邮箱格式不正确')])
    submit = SubmitField('立即注册')

    # 自定义字段验证
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户已存在，请选用其它用户名')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已注册，请选用其它邮箱地址')


class LoginForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired()])
    password = PasswordField('密码',validators=[DataRequired()])
    submit = SubmitField('登录')
    remember = BooleanField('记住我')


class ChangePasswordForm(FlaskForm):
    oldpassword = PasswordField('旧密码',validators=[DataRequired()])
    newpassword = PasswordField('新密码', validators=[Length(6, 20, message='密码长度必须在6~20个字符之间')])
    confirm1 = PasswordField('确认密码', validators=[EqualTo('newpassword', message='两次密码不一致')])
    submit = SubmitField('立即修改')

#修改头像表单
class IconForm(FlaskForm):
    icon = FileField('头像',validators=[FileAllowed(photos,message='只能上传图片'),FileRequired('请选择文件')])
    submit = SubmitField('保存')



#修改邮箱
class ChangeMailForm(FlaskForm):
    password = PasswordField('密码',validators=[DataRequired()])
    email = StringField('新邮箱',validators=[Email(message="邮箱的格式不正确")])
    submit = SubmitField('立刻修改')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已注册，请选用其它邮箱地址')
#找回密码
class FindpwdForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    submit = SubmitField('立刻找回')

    # 自定义字段验证
    def validate_username(self, field):
        if  not User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户还未注册')
class ResetPasswordForm(FlaskForm):
    newpassword = PasswordField('新密码', validators=[Length(6, 20, message='密码长度必须在6~20个字符之间')])
    confirm1 = PasswordField('确认密码', validators=[EqualTo('newpassword', message='两次密码不一致')])
    submit = SubmitField('立即重置')