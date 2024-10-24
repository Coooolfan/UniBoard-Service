from django.db import models


class NoteFile(models.Model):
    # id列会自动添加
    file = models.FileField(upload_to='note_file/', verbose_name="文件")
    insert_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["update_time"]),
        ]
