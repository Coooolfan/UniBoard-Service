# UniBoard-Service

Connect and view all your device (service).

Only for Linux, this project is not supported on Windows.

# 此分支正在使用Django 5重构项目……

### API doc

http://example.com/api/swagger/

##### note

##### for Developer

```shell
# 启动消息队列
# for linux
celery -A UniBoard worker -l INFO
# 启动Django服务
python manage.py runserver
```

```shell
# 初始化celery数据库
python manage.py migrate django_celery_results
# 生成迁移文件
python manage.py makemigrations 
# 执行迁移文件
python manage.py migrate 
```
