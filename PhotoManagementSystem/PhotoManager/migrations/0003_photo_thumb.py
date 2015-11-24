# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PhotoManager', '0002_auto_20151019_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='thumb',
            field=models.ImageField(default=1, upload_to=b'photos/%Y/%m/%d/thumb'),
            preserve_default=False,
        ),
    ]
