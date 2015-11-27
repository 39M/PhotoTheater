# coding=utf-8
import os
import random
from datetime import datetime
from django.core.files import File
from PhotoManager.models import *
from pytz import timezone

TIME_ZONE = timezone('Asia/Shanghai')

Comment.objects.all().delete()
Photo.objects.all().delete()
Album.objects.all().delete()

user = User.objects.filter(username='admin')[0]

Album.objects.create(
    user=user,
    name='Default',
)

for i in range(4):
    a = Album(
        user=user,
        name='Album' + str(i + 1),
        # create_date=timezone.now(),
        # update_date=timezone.now(),
    )
    a.save()
albums = Album.objects.filter(user=user)

files = os.listdir('tools/')
files.remove('data_generator.py')
for img in files:
    img.decode('utf-8')
    year = str(random.randint(2010, 2015))
    month = str(random.randint(1, 12)).zfill(2)
    day = str(random.randint(1, 28)).zfill(2)
    date_str = year + '-' + month + '-' + day
    p = Photo(
        album=albums[random.randint(0, len(albums) - 1)],
        name=img.split('.')[0],
        description=img.split('.')[0],
        shot_date=TIME_ZONE.localize(datetime.strptime(date_str, '%Y-%m-%d')),
        latitude=random.uniform(45, 46),
        longitude=random.uniform(126, 127),
    )
    tmp = File(open('tools/' + img, 'rb'))
    p.source = tmp
    p.origin_source = tmp
    p.thumb = tmp
    # p.source.save(img, File(open('tools/'+img, 'r')))
    # p.thumb.save(img, File(open('tools/'+img, 'r')))
    # p.origin_source.save(img, File(open('tools/'+img, 'r')))
    p.save()
