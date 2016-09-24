from django.db import models
from django.utils.translation import ugettext_lazy as _
from .user import Task


class Request(models.Model):
    REQUEST_STATUSES = ((0, 'Pending'), (1, 'Approved'), (2, 'Declined'))
    REQUEST_TYPES = ((0, 'Sell'), (1, 'Task'))

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
