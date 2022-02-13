from datetime import datetime

from django.db import models
from django.utils import timezone

# Create your models here.


class TimeStampModel(models.Model):

    created_at = models.DateTimeField(
        verbose_name="created_at", db_index=True, default=timezone.now
    )
    modified_at = models.DateTimeField(verbose_name="updated_at", auto_now=True)

    class Meta:
        abstract = True
