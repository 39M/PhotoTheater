# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PhotoManager', '0008_auto_20151125_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(editable=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='update_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='photo',
            name='update_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='photo',
            name='upload_date',
            field=models.DateTimeField(editable=False),
        ),
    ]
