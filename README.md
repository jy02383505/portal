### 目录结构 ###
- base 基础模块(用户管理 域名管理)
- cdn cdn加速模块
- common 常用方法,交互返回信息,后台api通信
- excel 生成下载excel文件路径
- security 安全cdn模块

### 启动 ###
> python manage.py runserver 0.0.0.0:8888 --settings=fuse_nova.settings.customer_settings 本地开发客户端模块启动

> python manage.py runserver 0.0.0.0:8888 --settings=fuse_nova.settings.admin_settings 本地开发管理端模块启动

> python manage.py runserver 0.0.0.0:8888 --settings=fuse_nova.settings.customer_settings_pro 线上测试客户端模块启动

> python manage.py runserver 0.0.0.0:8888 --settings=fuse_nova.settings.admin_settings_pro 线上测试管理端模块启动
# portal
