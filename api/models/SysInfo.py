from django.db import models


# Create your models here.
class SysInfo(models.Model):
    # id列会自动添加
    name = models.CharField(max_length=255)
    value = models.TextField()
