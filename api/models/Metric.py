from django.db import models


# 用来存储所有可能的监控指标，如CPU、内存、网络延迟等
class Metric(models.Model):
    class Type(models.IntegerChoices):
        number = 1, "number"
        string = 2, "string"

    # id列会自动添加
    name = models.CharField(max_length=64)
    # number/String
    type = models.IntegerField(choices=Type.choices)
    # 单位
    unit = models.CharField(max_length=16)
    desc = models.CharField(max_length=255)
