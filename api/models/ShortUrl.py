from django.db import models


class ShortUrl(models.Model):
    long_url = models.TextField(db_index=True)
    short_url = models.TextField(unique=True)
    gmt_create = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
