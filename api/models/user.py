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
    full_name = models.CharField(max_length=255, default='')
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

    balance = models.IntegerField(_('balance'), default=0)
    rating = models.IntegerField(_('rating'), default=0)
    phone = models.CharField(_('phone'), null=True, max_length=255)
    avatar = models.FileField(_('avatar'), upload_to='uploads/users/')

    achievements = models.ManyToManyField(
        Achievement,
        related_name='users'
    )

    def __str__(self):
        return '%s <%s>' % (self.full_name, self.email)

    def get_short_name(self):
        return self.full_name

    def get_level(self):
        return Level.objects \
            .filter(start_count__gte=self.rating) \
            .order_by('start_count').first()

    def get_full_name(self):
        return self.full_name

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
    pic = models.FileField('uploads/tasks/')


class TaskStatus(models.Model):
    user = models.ForeignKey(User, related_name='tasks',
                             on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)
