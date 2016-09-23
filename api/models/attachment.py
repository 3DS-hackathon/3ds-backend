from django.db import models
from .request import Request


class Attachment(models.Model):
    file = models.FileField(upload_to='uploads/attachments/')
    mime_type = models.CharField(null=True)
    request = models.ForeignKey(
        Request,
        on_delete=models.CASCADE,
        related_name='attachments'
    )
