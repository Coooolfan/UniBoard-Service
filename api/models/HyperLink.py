from django.db import models


class HyperLink(models.Model):
    icon = models.ImageField(upload_to='hyperlink_icon/', verbose_name="图标")
    title = models.CharField(max_length=100, verbose_name="标题")
    desc = models.CharField(max_length=255, verbose_name="描述")
    url = models.URLField(verbose_name="链接")
    # 默认淡灰色, 预留长度
    color = models.CharField(max_length=16, verbose_name="颜色", default="#f2f2f2")
