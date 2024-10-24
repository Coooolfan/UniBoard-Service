from django.db import models


class Note(models.Model):
    # id列会自动添加
    title = models.TextField()
    value = models.TextField()
    insert_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["update_time"]),
        ]
