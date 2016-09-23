from django.db import models
from django.utils.translation import ugettext_lazy as _
from .request import Request
from .user import Task


class BalanceLog(models.Model):
    ACTION_TYPES = ((0, 'income'), (1, 'outcome'))

    desc = models.TextField(_('description'), null=True)
    action = models.SmallIntegerField(_('action'), choices=ACTION_TYPES)
    delta_count = models.IntegerField(_('delta count'))

    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
