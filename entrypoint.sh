#!/bin/sh

set -e

upgrade_from_0_2_0() {
    echo "Upgrading to 0.2.1..."
#    生成迁移文件
    python manage.py makemigrations
#    执行迁移
    python manage.py migrate
    echo "0.2.1" > /app/media/version
}

# 检查是否需要初始化
if [ ! -f "/app/media/initialized" ]; then
    echo "Initializing Django database..."
    touch /app/api/migrations/__init__.py
    ls -l /app/api/migrations/
#    生成随机字符串
    SECRET_KEY=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 64)
    echo $SECRET_KEY > /app/media/SECRET_KEY
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
    touch /app/media/initialized
    echo "0.2.1" > /app/media/version
else
    echo "Skipping initialization..."
#    检查文件是否存在
    if [ ! -f "/app/media/version" ]; then
        INSTALLED_VERSION="0.2.0"
    else
        INSTALLED_VERSION=$(cat /app/media/version)
    fi
#    如果版本号是0.2.0，升级到0.2.1
    if [ "$INSTALLED_VERSION" = "0.2.0" ]; then
        upgrade_from_0_2_0
    fi
fi

# 执行传入的命令（在这里是运行 supervisord）
exec "$@"