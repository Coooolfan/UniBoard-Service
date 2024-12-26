# 使用官方的 Python 镜像
FROM python:3.12.4-slim-bookworm
# 设置容器内的工作目录
WORKDIR /app
# 复制当前目录的内容到容器中的 /app 目录
COPY . .
# 安装 requirements.txt 中指定的依赖
RUN pip install --no-cache-dir -r requirements.txt
# 如果 DEBUG 模式设置为 True，则将其改为 False
RUN sed -i 's/DEBUG = True/DEBUG = False/' /app/UniBoard/settings.py
# 设置环境变量
ENV PYTHONUNBUFFERED=1
# 安装 supervisord
RUN apt-get update && apt-get install -y --no-install-recommends supervisor \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
# 复制 supervisord 配置文件到容器中
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
# 复制入口脚本到容器中
COPY entrypoint.sh /entrypoint.sh
# 使入口脚本可执行
RUN chmod +x /entrypoint.sh
# 暴露端口 8000
EXPOSE 8000
# 容器启动时运行入口脚本
ENTRYPOINT ["/entrypoint.sh"]
# 运行应用程序和 celery
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]