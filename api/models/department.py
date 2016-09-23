from django.db import models
from django.utils.translation import ugettext_lazy as _


class Department(models.Model):
    name = models.CharField(_('name'))
    desc = models.TextField(_('description'), default='')
    rating = models.IntegerField(default=0)
    avatar = models.FileField(
        _('avatar'),
        null=True,
        upload_to='uploads/depts/'
    )