import os

from PIL import Image
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app, g
from flask_login import login_user, logout_user, login_required, current_user

from app.email import send_mail
from app.extensions import db, photos
from app.forms import RegisterForm,LoginForm,ChangePasswordForm,IconForm
from app.forms import ChangeMailForm,FindpwdForm,ResetPasswordForm
from app.models import User



user = Blueprint('user',__name__)



# 生成随机的字符串
def random_string(length=32):
    import random
    base_str = 'abcdefghijklmnopqrstuvwxyz1234567890'
    return ''.join(random.choice(base_str) for i in range(length))


@user.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # 根据表单数据创建用户对象
        u = User(username=form.username.data, password=form.password.data, email=form.email.data)
        # 将对象保存到数据库
        db.session.add(u)
        # 此时数据还没有保存到数据库中，没有id字段值，下面生成token时需要使用id
        # 因此等请求结束再提交时来不及的，故需要手动提交
        db.session.commit()
        # 发送用户的激活邮件
        # 生成用户激活的token
        token = u.generate_activate_token()
        send_mail(form.email.data, '账户激活', 'email/activate', username=form.username.data, token=token)
        # 给出flash提示消息
        flash('邮件已发送，请点击链接完成用户激活')
        return redirect(url_for('main.index'))
    return render_template('user/register.html', form=form)

@user.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if not u:
            flash('无效的用户名')
        elif not u.confirmed:
            flash('此账户还未激活')
            return redirect(request.args.get('next') or url_for('main.index'))
        elif u.verify_password(form.password.data):
            login_user(u)
            flash('登录成功')
            login_user(u, remember=form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('无效的密码')

    return render_template('user/login.html', form=form)
@user.route('/logout/')
def logout():
  	# 退出当前登录状态
    logout_user()
    flash('您已退出登录')
    return redirect(url_for('main.index'))
# 账户的激活
@user.route('/activate/<token>')
def activate(token):
    if User.check_activate_token(token):
        flash('账户已激活')
        return redirect(url_for('user.login'))
    else:
        flash('激活失败')
        return redirect(url_for('main.index'))
# 新邮箱的激活
@user.route('/newmailactivate/<token>')
def newmailactivate(token):
    if User.check_newmailactivate_token(token):
        flash('邮箱已修改')
        return redirect(url_for('user.profile'))
    else:
        flash('邮箱修改失败')
        return redirect(url_for('main.index'))
@user.route('/changepassword/',methods = ['GET','POST'])
# 路由保护，需要登录才可访问
@login_required
def changepassword():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username = current_user.username).first()
        if u.verify_password(form.oldpassword.data):
            u.password = form.newpassword.data
            db.session.add(u)
            flash('密码修成功')
            return redirect( url_for('main.index'))
        else:
            flash('无效的密码')

    return render_template('user/changepassword.html', form=form)

#修改邮箱
@user.route('/changemail/',methods = ['GET','POST'])
@login_required
def changemail():
    form = ChangeMailForm()
    if form.validate_on_submit():
        u = User.query.filter_by(id = current_user.id).first()
        if u.verify_password(form.password.data):
            # 发送用户的激活邮件
            # 生成用户激活的token
            token = u.generate_newmailactivate_token(newmail=form.email.data)
            send_mail(form.email.data, '邮箱修改', 'email/changemail', username=current_user.username, token=token)
            # 给出flash提示消息
            flash('邮件已发送，请点击链接完成邮箱修改')
            return redirect(url_for('main.index'))
    return render_template('user/changemail.html', form=form)
#密码找回
@user.route('/findbackpwd/',methods = ['GET','POST'])
def findbackpwd():
    form = FindpwdForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        token = u.generate_newmailactivate_token(newmail=form.email.data)
        send_mail(u.email, '重置密码', 'email/resetpwd', username=u.username,token=token)
        # 给出flash提示消息
        flash('邮件已发送，请点击链接完成密码重置')
    return render_template('user/findbackpwd.html',form=form)
#密码重置
@user.route('/resetpwd/', methods=['GET', 'POST'])
def resetpwd():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        pass
    render_template('user/findbackpwd.html')
#用户详情
@user.route('/profile/')
def profile():
    img_url = photos.url(current_user.icon)
    return render_template('user/profile.html',img_url = img_url)


#头像上传
@user.route('/icon/', methods=['GET', 'POST'])
def icon():
    form = IconForm()
    if form.validate_on_submit():
        #生成随机的文件名
        suffix = os.path.splitext(form.icon.data.filename)[1]
        filename = random_string() + suffix
        #保存文件
        photos.save(form.icon.data,name=filename)
        #拼接完整的路径名
        pathname = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],filename)
        #生成缩略图
        img = Image.open(pathname)
        #设置图片大小
        img.thumbnail((128,128))
        #重新保存
        img.save(pathname)
        #删除原来的头像，默认的除外
        if current_user.icon != 'default.jpg':
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],current_user.icon))
        #保存到数据库
        current_user.icon = filename
        db.session.add(current_user)
        flash('头像已修改')
    #获取头像的url
    img_url = photos.url(current_user.icon)
    return render_template('user/icon.html',form = form,img_url = img_url)