# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20160912_1541'),
    ]

    operations = [
        migrations.CreateModel(
            name='Piece',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('pieceAA', models.ImageField(width_field='pieceAAwidth', upload_to='documents/%Y/%m/%d', height_field='pieceAAheight')),
                ('pieceAAstate', models.CharField(max_length=30, default='null')),
                ('pieceAAwidth', models.IntegerField(null=True)),
                ('pieceAAheight', models.IntegerField(null=True)),
            ],
        ),
    ]
