from django.db import models


class UserInfo(models.Model):
    VERSION_MAX_LENGTH = 50
    NAME_MAX_LENGTH = 100
    SLOGAN_MAX_LENGTH = 255

    id = models.IntegerField(primary_key=True, default=1, editable=False)
    version = models.CharField(max_length=VERSION_MAX_LENGTH, verbose_name="版本")
    name = models.CharField(max_length=NAME_MAX_LENGTH, verbose_name="姓名")
    name_font = models.FileField(upload_to='fonts/', verbose_name="姓名字体")
    profile = models.TextField(verbose_name="简介")
    contacts = models.JSONField(verbose_name="联系方式")
    slogan = models.CharField(max_length=SLOGAN_MAX_LENGTH, verbose_name="Slogan")
    avatar = models.FileField(upload_to='avatars/', verbose_name="头像")
    banner = models.FileField(upload_to='banners/', verbose_name="横幅图")

    class Meta:
        verbose_name = "系统信息"
        verbose_name_plural = "系统信息"

    def save(self, *args, **kwargs):
        self.pk = 1
        super(UserInfo, self).save(*args, **kwargs)

    def __str__(self):
        return f"系统信息 (ID: {self.pk})"
