from django.db import models
from django.utils import timezone

class Call(models.Model):
    submitted_at = models.DateTimeFieldd(efault=timezone.now)
    # headers = hstore
    # data = hstore
