from django.db import models


class Note(models.Model):
    # id列会自动添加
    title = models.CharField(max_length=255)
    value = models.CharField()
    insert_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["update_time"]),
        ]
