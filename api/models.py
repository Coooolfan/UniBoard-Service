from django.db import models


# Create your models here.
# 创建一个表用于存储受信任设备的ID
class TrustedDevice(models.Model):
    deviceID = models.CharField(max_length=100, primary_key=True, )

    class Meta:
        app_label = "api"
        indexes = [models.Index(fields=['deviceID'])]

    def __str__(self):
        return "trusted_devices"


# 创建一个被监控对象的表，其中定义了被监控对象的ID，名称，类别，状态列表
class MonitoredObjects(models.Model):
    objectID = models.IntegerField(primary_key=True, unique=True, )
    objectName = models.CharField(max_length=100, )
    category = models.CharField(max_length=100, )
    statusList = models.JSONField()

    class Meta:
        app_label = "api"
        indexes = [models.Index(fields=['objectID', 'objectName', 'category', 'statusList'])]

    def __str__(self):
        return "monitored_objects"


# 创建一个用于记录监控对象的状态的表，其中定义了被监控对象的ID，状态的时间戳，状态的值
class Status(models.Model):
    statusID = models.IntegerField(primary_key=True, unique=True, )
    objectID = models.IntegerField()
    insertStamp = models.DateTimeField(auto_created=True)
    repotyStamp = models.DateTimeField()
    status = models.JSONField()

    class Meta:
        app_label = "api"
        indexes = [models.Index(fields=['statusID', 'objectID', 'repotyStamp'])]

    def __str__(self):
        return "status"


class Configuration(models.Model):
    name = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.name
