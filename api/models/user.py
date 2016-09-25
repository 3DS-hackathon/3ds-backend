import datetime
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django.utils.translation import ugettext_lazy as _

from .department import Department
from .achievement import Achievement


class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            role=User.ROLE_TYPES[0][0]
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            password=password
        )

        user.role = User.ROLE_TYPES[1][0]
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    ROLE_TYPES = (('rab', 'User'), ('vertuhai', 'Manager'))
    USERNAME_FIELD = 'email'

    objects = UserManager()

    email = models.CharField(max_length=255, unique=True, db_index=True)
    full_name = models.CharField(max_length=255, default='Аноним')
    role = models.CharField(
        _('user role'),
        max_length=10,
        choices=ROLE_TYPES,
        default=ROLE_TYPES[0][0]
    )
    department = models.ForeignKey(
        Department,
        null=True,
        on_delete=models.SET_NULL,
        related_name='users'
    )

    tasks = models.ManyToManyField(
        'Task',
        related_name='users',
        through='TaskStatus',
        through_fields=('user', 'task')
    )

    @property
    def achievements(self):
        from .request import Request
        tasks = Task.objects.filter(
            requests__user=self,
            requests__status=Request.REQUEST_STATUSES[1][0]
        )
        return Achievement.objects.filter(tasks__in=tasks)

    @property
    def rating(self):
        from .request import Request
        start_day = datetime.date.today().replace(day=1)
        tasks = Task.objects.filter(
            requests__user=self,
            requests__status=Request.REQUEST_STATUSES[1][0],
            statuses__done_timestamp__gte=start_day
        )
        return tasks.aggregate(models.Sum('experience'))['experience__sum'] \
            or 0

    phone = models.CharField(_('phone'), null=True, max_length=255)
    avatar = models.FileField(_('avatar'), upload_to='upload/users/%Y/%m/%d/')

    def __str__(self):
        return '%s <%s>' % (self.full_name, self.email)

    def get_short_name(self):
        return self.full_name

    def get_level(self):
        return Level.objects \
            .filter(start_count__gte=self.rating) \
            .order_by('start_count').first()

    def get_balance(self):
        from .balance import BalanceLog

        log = BalanceLog.objects.filter(request__user=self)
        income = log.filter(action=BalanceLog.ACTION_TYPES[0][0]).aggregate(
            models.Sum('delta_count')
        )['delta_count__sum'] or 0
        outcome = log.filter(action=BalanceLog.ACTION_TYPES[1][0]).aggregate(
            models.Sum('delta_count')
        )['delta_count__sum'] or 0

        return income - outcome

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.role == self.ROLE_TYPES[1][0]


class Level(models.Model):
    level = models.SmallIntegerField()
    name = models.CharField(max_length=255)
    start_count = models.IntegerField()
    end_count = models.IntegerField()

    def __str__(self):
        return self.name


class Task(models.Model):
    TASK_TYPES = (('count', 'Count'), ('task', 'Task'))

    name = models.CharField(_('name'), max_length=255)
    desc = models.TextField(_('description'), default='')
    type = models.CharField(
        _('type'),
        max_length=10,
        choices=TASK_TYPES,
        default=TASK_TYPES[0][0]
    )

    total_count = models.IntegerField(default=0)
    experience = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

    start_timestamp = models.DateTimeField(null=True)
    end_timestamp = models.DateTimeField(null=True)

    achievements = models.ManyToManyField(Achievement, related_name='tasks')
    pic = models.FileField('upload/tasks/%Y/%m/%d/')

    def __str__(self):
        return self.name


class TaskStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='statuses')
    done_timestamp = models.DateField(null=True, blank=True)
    progress = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Task status'
        verbose_name_plural = 'Statuses of tasks'

    @classmethod
    def create(cls, user, task):
        return TaskStatus.objects.get_or_create(user=user, task=task)

    @classmethod
    def remove(cls, user, task):
        TaskStatus.objects.get(user=user, task=task).delete()

    @classmethod
    def set_done_timestamp(cls, user, task):
        status = cls.objects.get(user=user, task=task)
        status.done_timestamp = datetime.date.today()
        status.save()

    @classmethod
    def remove_done_timestamp(cls, user, task):
        status = cls.objects.get(user=user, task=task)
        status.done_timestamp = None
        status.save()

