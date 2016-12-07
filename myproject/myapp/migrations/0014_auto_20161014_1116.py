# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_auto_20161008_1326'),
    ]

    operations = [
        migrations.RenameField(
            model_name='piece',
            old_name='created_date',
            new_name='submit_date',
        ),
        migrations.RemoveField(
            model_name='document',
            name='adminpassword',
        ),
        migrations.RemoveField(
            model_name='piece',
            name='piecepassword',
        ),
        migrations.AddField(
            model_name='piece',
            name='xpixelposition',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='piece',
            name='ypixelposition',
            field=models.IntegerField(null=True),
        ),
    ]
