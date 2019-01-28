# 说明书册

## 项目结构说明

```json
├── blog
│   ├── app
│   │   ├── config.py //配置文件
│   │   ├── email.py //邮件发送
│   │   ├── extensions.py //项目初始化脚本
│   │   ├── forms //Flask-wtf表单
│   │   │   ├── __init__.py
│   │   │   ├── posts.py
│   │   │   └── user.py
│   │   ├── __init__.py
│   │   ├── models //数据库模型
│   │   │   ├── __init__.py
│   │   │   ├── posts.py
│   │   │   └── user.py
│   │   ├── static //静态文件
│   │   │   ├── css
│   │   │   ├── img
│   │   │   │   └── tear.jpg
│   │   │   ├── js
│   │   │   ├── upload
│   │   │   │   ├── default.jpg
│   │   │   └── weibo.ico
│   │   ├── templates  //模板文件
│   │   │   ├── common
│   │   │   │   ├── base.html
│   │   │   │   └── macro.html
│   │   │   ├── email
│   │   │   │   ├── activate.html
│   │   │   │   ├── activate.txt
│   │   │   │   ├── changemail.html
│   │   │   │   ├── changemail.txt
│   │   │   │   ├── resetpwd.html
│   │   │   │   └── resetpwd.txt
│   │   │   ├── errors
│   │   │   │   └── 404.html
│   │   │   ├── main
│   │   │   │   └── index.html
│   │   │   ├── posts
│   │   │   │   └── myposts.html
│   │   │   └── user
│   │   │       ├── changemail.html
│   │   │       ├── changepassword.html
│   │   │       ├── findbackpwd.html
│   │   │       ├── icon.html
│   │   │       ├── login.html
│   │   │       ├── profile.html
│   │   │       ├── register.html
│   │   │       └── resetpwd.html
│   │   └── views  //视图函数
│   │       ├── __init__.py
│   │       ├── main.py
│   │       ├── posts.py
│   │       └── user.py
│   ├── manage.py //项目管理文件
│   ├── migrations  //数据迁移文件
│   ├── requirement.txt  //依赖包list
│   └── test //测试监本目录
└── README.md

```



> 首先在blog/app/config.py内填写相关的邮箱服务器信息

## 数据库迁移（初次运行项目要先进行数据库迁移）

以上三步完成mondel定义的表结构向数据库的迁移。并且会在项目下生成migrations/目录，保存数据库每次变更的内容。

1. 创建数据库表

   ```shell
   python manage.py db init
   ```

2. 提交修改

   ```
   python manage.py db migrate
   ```

3. 执行修改

   ```
   python manage.py db upgrage
   ```

**注：**若变更数据库则删除migrations目录，重新进行迁移

## 启动

```shell
# 在manage.py的目录下
python manage.py runserver 
```

