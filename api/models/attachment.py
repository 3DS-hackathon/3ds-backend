from django.db import models


class Attachment(models.Model):
    file = models.FileField(upload_to='uploads/attachments/')
    mime_type = models.CharField(null=True)
