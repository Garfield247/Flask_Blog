from flask import current_app, flash

from app.extensions import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
# 导入生成token的类
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# 导入token解析时的异常
from itsdangerous import BadSignature, SignatureExpired
# 导入UserMixin类
from flask_login import UserMixin

from .posts import Posts


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64),unique=True)
    confirmed = db.Column(db.Boolean,default=False)
    #头像
    icon = db.Column(db.String(40),default='default.jpg')
    #再领易模型中添加一个反向的引用
    #参数1：关联的模型名
    #参数2：backref在关联的模型中动态添加的字段
    #加载方式：dynamic,不加载，但是提供记录的查询
    #若使用一对一，添加uselist=Flase
    posts = db.relationship('Posts',backref = 'user',lazy= 'dynamic')

    #收藏
    favorites = db.relationship('Posts',secondary='collections',backref = db.backref('users',lazy='dynamic'),lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('密码是不可读属性')

    #设置密码，加密存储
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
    #密码校验
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    # 生成激活的token
    def generate_activate_token(self, expires_in=3600):   #到期时间为3600秒
        # 创建用于生成token的类，需要传递秘钥和有效期
        s = Serializer(current_app.config['SECRET_KEY'], expires_in)
        # 生成包含有效信息(必须是字典数据)的token字符串
        return s.dumps({'id': self.id})
    # 生成修改邮箱的token
    def generate_newmailactivate_token(self,newmail, expires_in=3600):   #到期时间为3600秒
        # 创建用于生成token的类，需要传递秘钥和有效期
        s = Serializer(current_app.config['SECRET_KEY'], expires_in)
        # 生成包含有效信息(必须是字典数据)的token字符串
        return s.dumps({'id': self.id,'newmail':newmail})

    # 账户激活，因为激活时还不知道是哪个用户
    @staticmethod
    def check_activate_token(token):
       s = Serializer(current_app.config['SECRET_KEY'])
       try:
           data = s.loads(token)   #解析token
       except BadSignature:
           flash('无效的token')
           return False
       except SignatureExpired:
           flash('token已失效')
           return False
       user = User.query.get(data.get('id'))
       if not user:
           flash('激活的账户不存在')
           return False
       if not user.confirmed:  # 没有激活才需要激活
           user.confirmed = True
           db.session.add(user)
       return True
    # 邮箱修改确认
    @staticmethod
    def check_newmailactivate_token(token):
       s = Serializer(current_app.config['SECRET_KEY'])
       try:
           data = s.loads(token)   #解析token
       except BadSignature:
           flash('无效的token')
           return False
       except SignatureExpired:
           flash('token已失效')
           return False
       user = User.query.get(data.get('id'))
       if not user:
           flash('激活的账户不存在')
           return False
       user.email = data.get('newmail')
       return True

    # 判断是否收藏指定帖子
    def is_favorite(self, pid):
        # 获取该用户所有收藏的帖子列表
        favorites = self.favorites.all()
        posts = list(filter(lambda p: p.id == pid, favorites))
        if len(posts) > 0:
            return True
        return False
    # 收藏指定帖子
    def add_favorite(self, pid):
        p = Posts.query.get(pid)
        self.favorites.append(p)

    # 取消收藏指定帖子
    def del_favorite(self, pid):
        p = Posts.query.get(pid)
        self.favorites.remove(p)
#登录认证的回调
@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))
