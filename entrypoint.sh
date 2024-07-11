#!/bin/sh

set -e

# 检查是否需要初始化
if [ ! -f "/app/initialized" ]; then
    echo "Initializing Django database..."
#    生成迁移文件
    python manage.py makemigrations
#    执行迁移
    python manage.py migrate
#    创建超级用户，从环境变量中获取用户名和密码
    python manage.py createsuperuser --noinput
#    复制默认的图片文件
    mkdir -p /app/media/avatars
    mkdir -p /app/media/banners
    cp /app/img/jonas-leupe-QA0pL9yfxk0-avatar.avif /app/media/avatars/jonas-leupe-QA0pL9yfxk0-avatar.avif
    cp /app/img/paul-pastourmatzis-kN_v2HFm7Tw-banner.avif /app/media/banners/paul-pastourmatzis-kN_v2HFm7Tw-banner.avif
#    创建默认userinfo
    python manage.py loaddata /app/default_userinfo.json
    touch /app/initialized
else
    echo "Skipping initialization..."
fi

# 执行传入的命令（在这里是运行 supervisord）
exec "$@"