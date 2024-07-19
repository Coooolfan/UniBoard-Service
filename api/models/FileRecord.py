from django.db import models


class FileRecord(models.Model):
    public = 1
    private = 2
    password = 3

    permission_choices = (
        (public, "public"),
        (private, "private"),
        (password, "password"),
    )

    file_name = models.CharField(max_length=100, verbose_name="文件名")
    file = models.FileField(upload_to='file/', verbose_name="文件")
    desc = models.TextField(blank=True, verbose_name="文件描述")
    permission = models.IntegerField(choices=permission_choices, default=private, verbose_name="权限")
    password = models.CharField(max_length=16, verbose_name="密码", null=True, blank=True, default=None)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
