from django.db import models
from django.contrib.auth.models import User as UserModel
from django.utils.translation import ugettext_lazy as _

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
    phone = models.CharField(_('phone'), null=True, max_length=255)
    avatar = models.FileField(_('avatar'), upload_to='uploads/users/')

    tasks = models.ManyToManyField(
        'Task',
        null=True,
        related_name='users',
        through='TaskStatus',
        through_fields=('user', 'task')
    )
    achievements = models.ManyToManyField(
        Achievement,
        null=True,
        related_name='users'
    )


class Task(models.Model):
    TASK_TYPES = ((0, 'count'), (1, 'task'))

    name = models.CharField(_('name'), max_length=255)
    desc = models.TextField(_('description'), default='')
    type = models.SmallIntegerField(
        _('type'),
        choices=TASK_TYPES,
        default=TASK_TYPES[0][0]
    )

    total_count = models.IntegerField(default=0)
    achievements = models.ManyToManyField(Achievement, related_name='tasks')


class TaskStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)
