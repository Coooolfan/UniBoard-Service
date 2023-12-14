# 使用官方 Python 镜像作为基础镜像
FROM python:3.11.7-alpine3.19

# 安装 git
RUN apk add --no-cache git

# 设置工作目录
WORKDIR /app

# 从git上拉取项目代码到容器的工作目录
RUN git clone https://github.com/Coooolfan/UniBoard-Service
WORKDIR /app/UniBoard-Service

# 安装项目依赖
RUN pip install -r requirements.txt

# 创建启动脚本
RUN echo '#!/bin/sh' > start.sh && \
    echo 'python manage.py makemigrations' >> start.sh && \
    echo 'python manage.py migrate' >> start.sh && \
    echo 'python manage.py refresh --all true' >> start.sh && \
    echo 'python manage.py runserver --noreload 0.0.0.0:8000' >> start.sh && \
    chmod +x start.sh

# 定义容器启动时执行的命令
CMD ["sh", "start.sh"]