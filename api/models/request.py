from django.db import models
from django.utils.translation import ugettext_lazy as _
from .task import Task


class Request(models.Model):
    REQUEST_STATUSES = ((0, 'pending'), (1, 'approved'), (2, 'declined'))
    REQUEST_TYPES = ((0, 'sell'), (1, 'task'))

    delta_balance = models.IntegerField(_('balance delta'))
    status = models.SmallIntegerField(
        _('status'),
        choices=REQUEST_STATUSES,
        default=REQUEST_STATUSES[0][0]
    )
    type = models.SmallIntegerField(
        _('type'),
        choices=REQUEST_TYPES,
        default=REQUEST_TYPES[0][0]
    )
    task = models.ForeignKey(
        Task,
        null=True,
        on_delete=models.SET_NULL,
        related_name='requests'
    )
