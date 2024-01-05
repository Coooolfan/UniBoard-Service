from django.db import models


# Create your models here.
# 创建一个表用于存储受信任设备的ID
class TrustedDevice(models.Model):
    deviceID = models.CharField(max_length=100, primary_key=True, )

    class Meta:
        app_label = "api"
        indexes = [models.Index(fields=['deviceID'])]

    def __str__(self):
        return "deviceID: " + f"{self.deviceID}"


# 创建一个被监控对象的表，其中定义了被监控对象的ID，名称，类别，状态列表
class MonitoredObjects(models.Model):
    objectID = models.IntegerField(primary_key=True, unique=True, )
    objectName = models.CharField(max_length=100, )
    category = models.CharField(max_length=100, )
    statusList = models.JSONField()
    token = models.CharField(max_length=100, )

    class Meta:
        app_label = "api"
        indexes = [models.Index(fields=['objectID', 'objectName', 'category', 'statusList'])]

    def __str__(self):
        return "objectID: " + f"{self.objectID}" + ", objectName: " + f"{self.objectName}" + ", category: " + \
            f"{self.category}" + ", statusList: " + f"{self.statusList}" + ", token: " + f"{self.token}"


# 创建一个用于记录监控对象的状态的表，其中定义了被监控对象的ID，状态的时间戳，状态的值
class Status(models.Model):
    statusID = models.IntegerField(primary_key=True, unique=True, )
    objectID = models.IntegerField()
    insertStamp = models.DateTimeField(auto_now_add=True)
    reportStamp = models.DateTimeField()
    status = models.JSONField()

    class Meta:
        app_label = "api"
        indexes = [models.Index(fields=['statusID', 'objectID', 'reportStamp'])]

    def __str__(self):
        return "statusID: " + f"{self.statusID}" + ", objectID: " + f"{self.objectID}" + ", insertStamp: " + \
            f"{self.insertStamp}" + ", reportStamp: " + f"{self.reportStamp}" + ", status: " + f"{self.status}"


class PeriodStatus(models.Model):
    statusID = models.IntegerField(primary_key=True, unique=True, )
    objectID = models.IntegerField()
    startStamp = models.DateTimeField()
    endStamp = models.DateTimeField()
    status = models.JSONField()

    class Meta:
        app_label = "api"
        indexes = [models.Index(fields=['statusID', 'objectID'])]

    def __str__(self):
        return "statusID: " + f"{self.statusID}" + ", objectID: " + f"{self.objectID}" + ", startStamp: " + \
            f"{self.startStamp}" + ", endStamp: " + f"{self.endStamp}" + ", status: " + f"{self.status}"


class Configuration(models.Model):
    name = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=255)

    def __str__(self):
        return "name: " + f"{self.name}" + ", value: " + f"{self.value}"
