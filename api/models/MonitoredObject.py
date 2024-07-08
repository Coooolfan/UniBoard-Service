from django.db import models


class MonitoredObject(models.Model):
    # id列会自动添加
    name = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
