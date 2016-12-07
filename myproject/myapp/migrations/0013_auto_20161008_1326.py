# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_auto_20160921_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='piece',
            name='image',
            field=models.ImageField(width_field='width', height_field='height', upload_to='pieces/%Y/%m/%d'),
        ),
    ]
