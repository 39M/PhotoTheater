from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):
    # the photo commented
    photo = models.ForeignKey('Photo')
    # comment content
    content = models.TextField()
    # comment date
    date = models.DateTimeField()
    # comment update date
    update_date = models.DateTimeField()


class Photo(models.Model):
    # photo album
    album = models.ForeignKey('Album')
    # photo name
    name = models.CharField(max_length=64)
    # photo date
    shot_date = models.DateTimeField()
    # photo upload date
    upload_date = models.DateTimeField()
    # photo update date
    update_date = models.DateTimeField()
    # photo location latitude
    latitude = models.FloatField()
    # photo location longitude
    longitude = models.FloatField()
    # photo location text
    location_text = models.TextField()
    # photo emotion
    emotion = models.CharField(max_length=16)
    # photo origin file
    origin_source = models.ImageField(upload_to='photos/%Y/%m/%d')
    # photo newest file
    source = models.ImageField(upload_to='photos/%Y/%m/%d')


class Album(models.Model):
    # album owner
    user = models.ForeignKey(User)
    # album name
    name = models.CharField(max_length=64)
    # album create date
    create_date = models.DateTimeField()
    # album update date
    update_date = models.DateTimeField()