# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20160702_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='adminpassword',
            field=models.CharField(max_length=30, default='null'),
        ),
        migrations.AddField(
            model_name='document',
            name='image_height',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='image_width',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='docfile',
            field=models.ImageField(height_field='image_height', upload_to='documents/%Y/%m/%d', width_field='image_width'),
        ),
    ]
