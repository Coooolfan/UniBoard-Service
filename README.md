# UniBoard-Service

个人主页 + 导航页 + 笔记 + 短链接 + ……?

此仓库仅为后端代码，使用 Django
构建。并以Restful设计API。[前端仓库地址点此访问。](https://github.com/Coooolfan/UniBoard)

**详细介绍与部署请参照前端仓库的`README.md`文件**

### API doc

**这个版本没有API docs，正在寻求更好的方案**

~~http://example.com/api/swagger/~~

### for Developer

clone本仓库到本地后，运行sql目录下的docker-compose.yml文件，启动数据库服务。

然后依次执行以下命令即可启动后端服务

```shell
# 创建 环境（注意执行路径，会直接在当前路径下创建）
# virtualenv UniBoard-Service
# 激活 环境
# source ~/.virtualenvs/UniBoard-Service/bin/activate
pip install -r requirements.txt
# 生成迁移文件
python manage.py makemigrations 
# 执行迁移文件
python manage.py migrate 
# 导出默认的userInfo
# python manage.py dumpdata api.userinfo
# 导入默认的userInfo
python manage.py loaddata default_dumpdata.json
# 启动Django服务
python manage.py runserver 0.0.0.0:8001
# 启动消息队列（开第二个终端） 仅适用于 Linux 
celery -A UniBoard worker -l INFO
```


build docker image

```shell
docker build -t coolfan1024/uniboard-service:latest .
```