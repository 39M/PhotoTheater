# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PhotoManager', '0011_auto_20151126_1807'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='photo',
        ),
        migrations.AddField(
            model_name='photo',
            name='filter_type',
            field=models.CharField(default=b'', max_length=64),
        ),
        migrations.AddField(
            model_name='photo',
            name='origin_thumb',
            field=models.ImageField(default=0, upload_to=b'photos/thumb/origin'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='photo',
            name='origin_source',
            field=models.ImageField(upload_to=b'photos/origin'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='source',
            field=models.ImageField(upload_to=b'photos'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='thumb',
            field=models.ImageField(upload_to=b'photos/thumb'),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
