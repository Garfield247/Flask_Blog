from flask import Blueprint, jsonify, render_template, request, g
from flask_login import current_user
import os

from app.models import Posts

posts = Blueprint('posts', __name__)


# 参数最好是类型限定，向后传递时默认是字符串
@posts.route('/collect/<int:pid>')
def collect(pid):
    # 判断是否收藏过此贴
    if current_user.is_favorite(pid):
        # 取消收藏
        current_user.del_favorite(pid)
    else:
        # 收藏
        current_user.add_favorite(pid)
    return jsonify({'result': 'ok'})

@posts.route('/myposts/<int:uid>')
def myposts(uid):

    posts = Posts.query.filter_by(rid = 0).filter_by(uid=uid).order_by(Posts.timestamp.desc())
    page = request.args.get('page', 1, type=int)
    pagination = posts.paginate(page, per_page=2, error_out=False)
    posts = pagination.items
    return render_template('posts/myposts.html', posts=posts,pagination=pagination)