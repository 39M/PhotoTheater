# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PhotoManager', '0007_auto_20151125_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='create_date',
            field=models.DateTimeField(editable=False),
        ),
        migrations.AlterField(
            model_name='album',
            name='update_date',
            field=models.DateTimeField(),
        ),
    ]
