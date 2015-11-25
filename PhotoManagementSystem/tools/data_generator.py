# coding=utf-8
import os
import random
from django.utils import timezone
from django.core.files import File
from PhotoManager.models import *

Comment.objects.all().delete()
Photo.objects.all().delete()
Album.objects.all().delete()

user = User.objects.filter(username='admin')[0]

for i in range(5):
    a = Album(
        user=user,
        name='Album'+str(i+1),
        # create_date=timezone.now(),
        # update_date=timezone.now(),
    )
    a.save()
albums = Album.objects.filter(user=user)

files = os.listdir('tools/')
files.remove('data_generator.py')
for img in files:
    img.decode('utf-8')
    p = Photo(
        album=albums[random.randint(0, len(albums) - 1)],
        name=img.split('.')[0],
        # shot_date=timezone.now(),
        # upload_date=timezone.now(),
        # update_date=timezone.now(),
    )
    tmp = File(open('tools/' + img, 'rb'))
    p.source = tmp
    p.origin_source = tmp
    p.thumb = tmp
    # p.source.save(img, File(open('tools/'+img, 'r')))
    # p.thumb.save(img, File(open('tools/'+img, 'r')))
    # p.origin_source.save(img, File(open('tools/'+img, 'r')))
    p.save()
