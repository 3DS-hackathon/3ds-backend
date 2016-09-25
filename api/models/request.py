from django.db import models
from django.utils.translation import ugettext_lazy as _
from .user import Task, User, TaskStatus
from .balance import BalanceLog


class Request(models.Model):
    REQUEST_STATUSES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined')
    )
    REQUEST_TYPES = (('task', 'Task'),)

    status = models.CharField(
        _('status'),
        max_length=20,
        choices=REQUEST_STATUSES,
        default=REQUEST_STATUSES[0][0]
    )
    user = models.ForeignKey(User, related_name='requests')
    task = models.ForeignKey(Task, null=True, on_delete=models.SET_NULL,
                             related_name='requests')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_status = self.status

    def save(self, **kwargs):
        if self.status != self.__initial_status:
            if self.status == self.REQUEST_STATUSES[1][0]:
                self.__approve()
            elif self.status == self.REQUEST_STATUSES[2][0]:
                self.__decline()
        super().save(**kwargs)

    def __approve(self):
        BalanceLog.create(self)
        TaskStatus.set_done(self.user, self.task)

    def __decline(self):
        BalanceLog.remove(self)
        TaskStatus.remove_done(self.user, self.task)

    def __str__(self):
        return '%s of %s - %s' % (self.task.name,
                                  self.user.full_name,
                                  self.status)
