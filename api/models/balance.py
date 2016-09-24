from django.db import models
from django.utils.translation import ugettext_lazy as _
from .request import Request


class BalanceLog(models.Model):
    ACTION_TYPES = ((0, 'income'), (1, 'outcome'))

    desc = models.TextField(_('description'), null=True)
    action = models.SmallIntegerField(_('action'), choices=ACTION_TYPES)
    delta_count = models.IntegerField(_('delta count'))

    request = models.ForeignKey(Request, on_delete=models.CASCADE)

    @classmethod
    def create(cls, request, action='income', desc=None):
        return cls.objects.create(
            desc=desc,
            action=action,
            delta_count=request.task.price,
            request=request
        )
