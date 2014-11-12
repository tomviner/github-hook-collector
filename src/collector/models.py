from django.db import models
from django.contrib.postgres.fields import HStoreField
from django.utils import timezone


class Call(models.Model):
    submitted_at = models.DateTimeField(default=timezone.now)
    headers = HStoreField(default={})
    data = HStoreField(default={})
