from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Photo(models.Model):
    # photo album
    album = models.ForeignKey('Album')
    # photo name
    name = models.CharField(max_length=256)
    # photo date
    shot_date = models.DateTimeField()
    # photo upload date
    upload_date = models.DateTimeField(editable=False)
    # photo update date
    update_date = models.DateTimeField()
    # photo location latitude
    latitude = models.FloatField(null=True)
    # photo location longitude
    longitude = models.FloatField(null=True)
    # photo location text
    location_text = models.TextField(default='')
    # photo emotion
    emotion = models.CharField(max_length=16, default='')
    # photo description
    description = models.CharField(max_length=1024, default='')
    # photo filter type
    filter_type = models.CharField(max_length=64, default='')
    # photo newest file
    source = models.ImageField(upload_to='photos')
    # photo origin file
    origin_source = models.ImageField(upload_to='photos/origin')
    # photo thumb
    thumb = models.ImageField(upload_to='photos/thumb')
    # photo origin thumb
    origin_thumb = models.ImageField(upload_to='photos/thumb/origin')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.upload_date = timezone.now()
        self.update_date = timezone.now()
        super(Photo, self).save(*args, **kwargs)

    def delete(self, using=None):
        self.origin_source.delete()
        self.source.delete()
        self.origin_thumb.delete()
        self.thumb.delete()
        super(Photo, self).delete()


class Album(models.Model):
    # album owner
    user = models.ForeignKey(User)
    # album name
    name = models.CharField(max_length=64)
    # album create date
    create_date = models.DateTimeField(editable=False)
    # album update date
    update_date = models.DateTimeField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.create_date = timezone.now()
        self.update_date = timezone.now()
        super(Album, self).save(*args, **kwargs)
