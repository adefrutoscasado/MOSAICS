# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-16 13:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_document_mosaic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='piece',
            name='submit_date',
            field=models.DateTimeField(default='None'),
        ),
    ]
