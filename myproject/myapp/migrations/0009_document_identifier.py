# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_auto_20160912_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='identifier',
            field=models.CharField(default='null', max_length=8),
        ),
    ]
