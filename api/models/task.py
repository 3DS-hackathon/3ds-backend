from django.db import models
from django.utils.translation import ugettext_lazy as _
from .achievement import Achievement


class Task(models.Model):
    TASK_TYPES = ((0, 'count'), (1, 'task'))

    name = models.CharField(_('name'))
    desc = models.TextField(_('description'), default='')
    type = models.SmallIntegerField(
        _('type'),
        choices=TASK_TYPES,
        default=TASK_TYPES[0][0]
    )

    total_count = models.IntegerField(default=0)
    achievements = models.ManyToManyField(Achievement, related_name='tasks')
