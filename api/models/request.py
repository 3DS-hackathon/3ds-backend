from django.db import models
from django.utils.translation import ugettext_lazy as _
from .user import Task, User


class Request(models.Model):
    REQUEST_STATUSES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined')
    )
    REQUEST_TYPES = (('sell', 'Sell'), ('task', 'Task'))

    status = models.CharField(
        _('status'),
        max_length=20,
        choices=REQUEST_STATUSES,
        default=REQUEST_STATUSES[0][0]
    )
    type = models.CharField(
        _('type'),
        max_length=20,
        choices=REQUEST_TYPES
    )
    user = models.ForeignKey(User, related_name='requests')
    task = models.ForeignKey(Task, null=True, on_delete=models.SET_NULL,
                             related_name='requests')
