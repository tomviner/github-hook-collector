from django.contrib.postgres.fields import HStoreField
from django.db import models
from django.db.models import DateField, IntegerField, Transform
from django.utils import timezone


@DateField.register_lookup
class YearTransform(Transform):
    lookup_name = 'year'
    output_field = IntegerField()

    def as_sql(self, compiler, connection):
        lhs, params = compiler.compile(self.lhs)
        return "EXTRACT(YEAR FROM %s)" % lhs, params


class Call(models.Model):
    submitted_at = models.DateTimeField(default=timezone.now)
    headers = HStoreField(default={})
    data = HStoreField(default={})
