# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PhotoManager', '0012_auto_20151219_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='filter_type',
            field=models.CharField(default=b'origin', max_length=64),
        ),
    ]
