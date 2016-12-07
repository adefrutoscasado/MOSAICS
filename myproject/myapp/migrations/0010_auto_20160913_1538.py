# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_document_identifier'),
    ]

    operations = [
        migrations.AddField(
            model_name='piece',
            name='documentidentifier',
            field=models.CharField(default='null', max_length=8),
        ),
        migrations.AddField(
            model_name='piece',
            name='identifier',
            field=models.CharField(default='null', max_length=15),
        ),
        migrations.AddField(
            model_name='piece',
            name='piecepassword',
            field=models.CharField(default='null', max_length=30),
        ),
        migrations.AddField(
            model_name='piece',
            name='xposition',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='piece',
            name='yposition',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='piece',
            name='image',
            field=models.ImageField(width_field='width', upload_to='documents/%Y/%m/%d', height_field='height'),
        ),
    ]
