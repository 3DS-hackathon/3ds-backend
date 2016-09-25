from django.db import models
from django.utils.translation import ugettext_lazy as _


class Achievement(models.Model):
    name = models.CharField(_('name'), max_length=255)
    desc = models.TextField(_('description'))

    pic = models.FileField(upload_to='upload/achievements/%Y/%m/%d/')
    background_color = models.CharField(max_length=7, default='#ffffff')
    text_color = models.CharField(
        max_length=7,
        default='black',
        choices=(('black', 'black'), ('white', 'white'))
    )

    def __str__(self):
        return self.name
