from django.db import models
from django.utils.translation import ugettext_lazy as _


class BalanceLog(models.Model):
    ACTION_TYPES = (('income', 'Income'), ('outcome', 'Outcome'))

    desc = models.TextField(_('description'), null=True)
    action = models.CharField(_('action'), max_length=10, choices=ACTION_TYPES)
    delta_count = models.IntegerField(_('delta count'))

    request = models.ForeignKey('api.Request', on_delete=models.CASCADE)

    @classmethod
    def create(cls, request, action='income', desc=None):
        return cls.objects.create(
            desc=desc,
            action=action,
            delta_count=request.task.price,
            request=request
        )

    @classmethod
    def remove(cls, request):
        cls.objects.get(request=request).delete()

    def __str__(self):
        return 'Balance log for (%s)' % str(self.request)
