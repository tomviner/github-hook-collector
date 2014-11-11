from django.db import models
from django.utils import timezone

class Call(models.Model):
    submitted_at = models.DateTimeField(auto_now_add=True, default=timezone.now)
    # headers = hstore
    # data = hstore
