# UniBoard-Service

个人主页 + 导航页 + 笔记 + 短链接 + ……?

此仓库仅为后端代码，使用 Django 构建。并以Restful风格设计API。[前端仓库地址点此访问。](https://github.com/Coooolfan/UniBoard)

**详细介绍与部署请参照前端仓库的`README.md`文件**

### API doc

http://example.com/api/swagger/


### for Developer

```shell
# 激活虚拟环境
source ~/.virtualenvs/UniBoard-Service/bin/activate
# 启动消息队列
# for linux
celery -A UniBoard worker -l INFO
# 启动Django服务
python manage.py runserver
```

```shell
# 导出默认的userInfo
python manage.py dumpdata api.userinfo
# 导入默认的userInfo
python manage.py loaddata default_userinfo.json
# 初始化celery数据库
python manage.py migrate django_celery_results
# 生成迁移文件
python manage.py makemigrations 
# 执行迁移文件
python manage.py migrate 
```
