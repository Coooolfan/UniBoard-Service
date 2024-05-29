from django.db import models


# 用来存储监控对象和监控指标的关系
class ObjectMetric(models.Model):
    monitored_object_id = models.IntegerField(db_index=True)
    metric_id = models.IntegerField()

    class Meta:
        # 为了防止重复添加, 一个监控对象只能对应一个监控指标
        unique_together = ('monitored_object_id', 'metric_id')

    def __str__(self):
        return f'{self.monitored_object_id} - {self.metric_id}'
