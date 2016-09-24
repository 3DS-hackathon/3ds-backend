import mimetypes
from django.db import models
from .request import Request

mimetypes.init()


class Attachment(models.Model):
    path = models.FileField(upload_to='upload/attachments/%Y/%m/%d/')
    mime_type = models.CharField(null=True, max_length=255)
    request = models.ForeignKey(
        Request,
        null=True,
        on_delete=models.CASCADE,
        related_name='attachments'
    )

    def save(self, **kwargs):
        non_strict, _ = mimetypes.guess_type(self.path.name, strict=False)
        self.mime_type = non_strict
        super().save(**kwargs)

    def __str__(self):
        return self.path.name
