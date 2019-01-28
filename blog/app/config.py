#通用配置
import os
base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123456'

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.163.com'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'spchenguanghui@163.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')or '9010037317asd'

    #文件上传
    MAX_CONTENT_LENGTH = 8*1024*1024
    UPLOADED_PHOTOS_DEST = os.path.join(base_dir,'static/upload')

    @staticmethod
    def init_app(app):
        pass
#开发环境
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir,
                                                          'blog-dev.sqlite')
#测试环境
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir,
                                                              'blog-test.sqlite')

#生产环境
class PrductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir,
                                                          'blog.sqlite')
#配置字典
config = {
    'development':DevelopmentConfig,
    'testing': TestingConfig,
    'production': PrductionConfig,

    'default':DevelopmentConfig,
}