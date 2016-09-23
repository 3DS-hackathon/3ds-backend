from django.db import models
from django.utils.translation import ugettext_lazy as _


class Achievement(models.Model):
    name = models.CharField(_('name'))
    desc = models.TextField(_('description'))
    pic = models.FileField(upload_to='upload/achievements/')
