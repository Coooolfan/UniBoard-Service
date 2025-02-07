#!/usr/bin/env python

import os
import sys
import secrets
import shutil
import subprocess
from pathlib import Path

CURRENT_VERSION = "0.2.8"
APP_DIR = Path("/app")
MEDIA_DIR = APP_DIR / "media"


# 迁移数据库
def migrate_database():
    subprocess.run(["python", "manage.py", "makemigrations"], check=True)
    subprocess.run(["python", "manage.py", "migrate"], check=True)
    subprocess.run(["python", "manage.py", "populate_default_data"], check=True)


def generate_secret_key():
    return secrets.token_urlsafe(48)  # 生成一个64字节左右的随机字符串


def initialize():
    print("Initializing Django database...")

    # 创建必要的目录和文件
    (APP_DIR / "api/migrations/__init__.py").touch()

    # 生成密钥
    secret_key = generate_secret_key()
    with open(MEDIA_DIR / "SECRET_KEY", "w") as f:
        f.write(secret_key)

    migrate_database()

    # 创建超级用户
    subprocess.run(["python", "manage.py", "createsuperuser", "--noinput"], check=True)

    # 创建媒体目录
    (MEDIA_DIR / "avatars").mkdir(parents=True, exist_ok=True)
    (MEDIA_DIR / "banners").mkdir(parents=True, exist_ok=True)

    # 复制默认图片
    shutil.copy(
        APP_DIR / "img/jonas-leupe-QA0pL9yfxk0-avatar.avif",
        MEDIA_DIR / "avatars/jonas-leupe-QA0pL9yfxk0-avatar.avif",
    )
    shutil.copy(
        APP_DIR / "img/paul-pastourmatzis-kN_v2HFm7Tw-banner.avif",
        MEDIA_DIR / "banners/paul-pastourmatzis-kN_v2HFm7Tw-banner.avif",
    )

    # 标记初始化完成
    (MEDIA_DIR / "initialized").touch()
    with open(MEDIA_DIR / "version", "w") as f:
        f.write(CURRENT_VERSION)


def main():
    if not (MEDIA_DIR / "initialized").exists():
        initialize()
    else:
        print("Skipping initialization...")
        print("Checking for upgrades...")

        with open(MEDIA_DIR / "version") as f:
            installed_version = f.read().strip()

        if installed_version != CURRENT_VERSION:
            # 执行版本升级
            migrate_database()

            # 更新版本号
            with open(MEDIA_DIR / "version", "w") as f:
                f.write(CURRENT_VERSION)

        print("Launch Django and qcluster...")

    # 执行后续命令
    if len(sys.argv) > 1:
        os.execvp(sys.argv[1], sys.argv[1:])


if __name__ == "__main__":
    main()
