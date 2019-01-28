from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user

from app.extensions import db
from app.forms import PostsForm
from app.models import Posts
main = Blueprint('main',__name__)


@main.route('/',methods = ['GET','POST'])
def index():
    form = PostsForm()
    if form.validate_on_submit():
        #判断是否登录python
        if current_user.is_authenticated:
            u = current_user._get_current_object()
            p = Posts(content = form.content.data,user = u)
            db.session.add(p)
            return redirect(url_for('main.index'))
        else:
            flash('登录后才能发表')
            return redirect(url_for('user.login'))
    #读取帖子的信息
    # posts = Posts.query.filter_by(rid = 0).order_by(Posts.timestamp.desc()).all()
    page = request.args.get('page',1,type=int)
    pagination = Posts.query.filter_by(rid=0).order_by(Posts.timestamp.desc()).paginate(page,per_page=5,error_out=False)
    posts = pagination.items
    return render_template('main/index.html',form = form,posts =posts,pagination=pagination)
