# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('PhotoManager', '0010_auto_20151126_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='shot_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 26, 10, 7, 27, 111000, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
