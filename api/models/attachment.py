from mimetypes import MimeTypes
from django.db import models
from .request import Request


class Attachment(models.Model):
    path = models.FileField(upload_to='uploads/attachments/')
    mime_type = models.CharField(null=True, max_length=255)
    request = models.ForeignKey(
        Request,
        null=True,
        on_delete=models.CASCADE,
        related_name='attachments'
    )

    def save(self, **kwargs):
        types = MimeTypes()
        types.readfp(self.path)

        type_map = types.types_map[0]
        if type_map:
            self.mime_type = type_map.popitem()[1]
        super().save(**kwargs)
