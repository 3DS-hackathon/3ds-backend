from django.db import models
from django.utils.translation import ugettext_lazy as _
from .achievement import Achievement


class Department(models.Model):
    name = models.CharField(_('name'), max_length=255)
    desc = models.TextField(_('description'), default='')
    avatar = models.FileField(
        _('avatar'),
        null=True,
        upload_to='upload/depts/%Y/%m/%d/'
    )

    achievements = models.ManyToManyField(
        Achievement, db_constraint=models.CASCADE
    )

    @property
    def rating(self):
        from .user import TaskStatus
        exp = TaskStatus.objects.filter(
            user__in=self.users.all(),
            status='completed'
        ).aggregate(models.Sum('task__experience'))['task__experience__sum'] or 0
        users_count = self.users.count()
        return 0 if users_count == 0 else exp / users_count

    def __str__(self):
        return self.name
