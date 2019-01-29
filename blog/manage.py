import os
from flask_script import Manager,Server
from app import create_app
from flask_migrate import MigrateCommand
#获取配置
config_name = os.environ.get('FLASK_CONFIG') or 'default'

#创建实例
app = create_app(config_name)

#创建命令起动控制对象
manager = Manager(app)
# 添加数据库迁移命令
manager.add_command('db', MigrateCommand)
# 添加服务配置
manger.add_command('sunserver',Server(host='0.0.0.0',port=9527))

if __name__ == '__main__':
    manager.run()
