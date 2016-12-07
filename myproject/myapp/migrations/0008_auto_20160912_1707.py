# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_piece'),
    ]

    operations = [
        migrations.RenameField(
            model_name='piece',
            old_name='pieceAAheight',
            new_name='height',
        ),
        migrations.RenameField(
            model_name='piece',
            old_name='pieceAA',
            new_name='image',
        ),
        migrations.RenameField(
            model_name='piece',
            old_name='pieceAAstate',
            new_name='state',
        ),
        migrations.RenameField(
            model_name='piece',
            old_name='pieceAAwidth',
            new_name='width',
        ),
    ]
