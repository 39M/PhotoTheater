# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PhotoManager', '0006_auto_20151124_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='album',
            name='update_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='update_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='emotion',
            field=models.CharField(default=b'', max_length=16),
        ),
        migrations.AlterField(
            model_name='photo',
            name='location_text',
            field=models.TextField(default=b''),
        ),
        migrations.AlterField(
            model_name='photo',
            name='origin_source',
            field=models.ImageField(upload_to=b'photos/%Y/%m/%d/origin'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='update_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='upload_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
