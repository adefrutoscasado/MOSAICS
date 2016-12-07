# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_auto_20160914_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='document',
            name='owner',
            field=models.CharField(max_length=30, default='null'),
        ),
        migrations.AddField(
            model_name='piece',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='piece',
            name='owner',
            field=models.CharField(max_length=30, default='null'),
        ),
    ]
