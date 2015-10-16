# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('create_date', models.DateTimeField()),
                ('update_date', models.DateTimeField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('date', models.DateTimeField()),
                ('update_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('shot_date', models.DateTimeField()),
                ('upload_date', models.DateTimeField()),
                ('update_date', models.DateTimeField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('location_text', models.TextField()),
                ('emotion', models.CharField(max_length=16)),
                ('origin_source', models.ImageField(upload_to=b'')),
                ('source', models.ImageField(upload_to=b'')),
                ('album', models.ForeignKey(to='PhotoManager.Album')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='photo',
            field=models.ForeignKey(to='PhotoManager.Photo'),
        ),
    ]
