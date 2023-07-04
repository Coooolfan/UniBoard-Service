from django.db import models


# Create your models here.
# 创建一个表用于存储高级设备的ID
class TrustedDevice(models.Model):
    deviceID = models.CharField(max_length=100, primary_key=True, )

    class Meta:
        app_label = "api"

    def __str__(self):
        return "trusted_devices"
