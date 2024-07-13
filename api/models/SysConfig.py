from django.db import models


class SysConfig(models.Model):
    id = models.IntegerField(primary_key=True, default=1, editable=False)
    host = models.CharField(max_length=255, verbose_name="主机地址")
    TOTP_SECRET_KEY = models.TextField(verbose_name="TOTP密钥")

    class Meta:
        verbose_name = "系统设置"
        verbose_name_plural = "系统设置"

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SysConfig, self).save(*args, **kwargs)

    def __str__(self):
        return f"系统设置 (ID: {self.pk})"
