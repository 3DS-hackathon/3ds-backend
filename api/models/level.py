from django.db import models


class Level(models.Model):
    level = models.SmallIntegerField()
    name = models.CharField(max_length=255)
    start_count = models.IntegerField()
    end_count = models.IntegerField()