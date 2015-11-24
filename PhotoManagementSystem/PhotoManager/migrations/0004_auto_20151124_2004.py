# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('PhotoManager', '0003_photo_thumb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 24, 20, 4, 54, 966000), blank=True),
        ),
        migrations.AlterField(
            model_name='album',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 24, 20, 4, 54, 966000), blank=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 24, 20, 4, 54, 965000), blank=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 24, 20, 4, 54, 965000), blank=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='emotion',
            field=models.CharField(default=b'', max_length=16, blank=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='latitude',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='location_text',
            field=models.TextField(default=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='longitude',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='shot_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 24, 20, 4, 54, 965000), null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 24, 20, 4, 54, 965000), blank=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='upload_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 24, 20, 4, 54, 965000), blank=True),
        ),
    ]
