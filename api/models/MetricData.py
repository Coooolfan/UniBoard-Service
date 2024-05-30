from django.db import models


class MetricData(models.Model):
    # id列会自动添加
    monitor_object_id = models.IntegerField()
    insert_time = models.DateTimeField(auto_now_add=True)
    report_time = models.DateTimeField()
    delay = models.IntegerField()
    data = models.JSONField()

    class Meta:
        indexes = [
            models.Index(fields=["monitor_object_id"]),
        ]
