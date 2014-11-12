# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.contrib.postgres.fields.hstore


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submitted_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('data', django.contrib.postgres.fields.hstore.HStoreField(default={})),
                ('headers', django.contrib.postgres.fields.hstore.HStoreField(default={})),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
