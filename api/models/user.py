from django.db import models
from django.contrib.auth.models import User as UserModel
from django.utils.translation import ugettext_lazy as _

from .task import Task
from .department import Department
from .achievement import Achievement
from .level import Level


class User(UserModel):
    ROLE_TYPES = ((0, 'rab'), (1, 'vertuhai'))

    role = models.SmallIntegerField(
        _('user role'),
        choices=ROLE_TYPES,
        default=ROLE_TYPES[0][0]
    )
    department = models.ForeignKey(
        Department,
        null=True,
        on_delete=models.SET_NULL,
        related_name='users'
    )

    level = models.ForeignKey(Level, related_name='users')
    balance = models.IntegerField(_('balance'), default=0)
    rating = models.IntegerField(_('rating'), default=0)
    phone = models.CharField(_('phone'), null=True)
    avatar = models.FileField(_('avatar'), upload_to='uploads/users/')

    tasks = models.ManyToManyField(
        Task,
        null=True,
        related_name='users',
        through='TaskUserStatus',
        through_fields=('user', 'task')
    )
    achievements = models.ManyToManyField(
        Achievement,
        null=True,
        related_name='users'
    )


class TaskUserStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    complete_count = models.IntegerField(default=0)