# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PhotoManager', '0004_auto_20151124_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='create_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='album',
            name='update_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='update_date',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='latitude',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='longitude',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='origin_source',
            field=models.ImageField(upload_to=b'photos/%Y/%m/%d/origin'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='shot_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='update_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='photo',
            name='upload_date',
            field=models.DateTimeField(),
        ),
    ]
