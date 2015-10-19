# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PhotoManager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='origin_source',
            field=models.ImageField(upload_to=b'photos/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='source',
            field=models.ImageField(upload_to=b'photos/%Y/%m/%d'),
        ),
    ]
