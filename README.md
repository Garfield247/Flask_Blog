# Flask项目

### 项目需求

1. 用户注册、登录、激活
2. 用户信息管理
3. 博客发表、回复
4. 博客展示、分页展示
5. 收藏博客
6. 搜索、点赞、统计、排序、...

### 目录结构

```
project/
	app/					# 整个程序的包目录
		static/					# 静态资源文件
			js/						# JS脚本
			css/					# 样式表
			img/					# 图片
			favicon.ico				 # 网站图标
		templates/				# 模板文件
			common/					# 通用模板
			errors/					# 错误页面
			user/					# 用户模板
			posts/					# 帖子模板
			email/					# 邮件发送
		views/					# 视图文件
		models/					# 数据模型
		forms/					# 表单文件
		config.py				# 配置文件
		email.py				# 邮件发送
		extensions.py			# 各种扩展
	migrations/				# 数据库迁移目录
	tests/					# 测试单元
	.env/					# 虚拟环境
	requirements.txt		# 依赖包的列表
	manage.py				# 项目启动控制文件
```