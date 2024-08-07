from enum import Enum

from django.db import models


class FileRecord(models.Model):
    class Permission(Enum):
        PUBLIC = 1
        PRIVATE = 2
        PASSWORD = 3

    permission_choices = (
        (Permission.PUBLIC.value, "public"),
        (Permission.PRIVATE.value, "private"),
        (Permission.PASSWORD.value, "password"),
    )

    file_name = models.CharField(max_length=100, verbose_name="文件名")
    file = models.FileField(upload_to='file/', verbose_name="文件")
    share_code = models.CharField(max_length=16, verbose_name="分享码", null=True, blank=True, default=None,
                                  unique=True, db_index=True)
    desc = models.TextField(blank=True, verbose_name="文件描述")
    permission = models.IntegerField(choices=permission_choices, default=Permission.PRIVATE.value, verbose_name="权限")
    password = models.CharField(max_length=16, verbose_name="密码", null=True, blank=True, default=None)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    count = models.IntegerField(default=0, verbose_name="下载次数")
