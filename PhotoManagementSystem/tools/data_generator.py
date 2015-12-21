# coding=utf-8
import os

print os.path.abspath(os.path.curdir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PhotoManagementSystem.settings")
from PhotoManager.models import *

import random
from datetime import datetime
from django.core.files import File
from pytz import timezone
from PIL import Image

TIME_ZONE = timezone('Asia/Shanghai')

photos = Photo.objects.all()
for photo in photos:
    photo.delete()
Album.objects.all().delete()

user = User.objects.filter(username='admin')
if user:
    user = user[0]
else:
    user = User.objects.create_superuser(username='admin', email='', password='admin')

Album.objects.create(
        user=user,
        name='Default',
)

for i in range(4):
    a = Album(
            user=user,
            name='Album' + str(i + 1),
    )
    a.save()
albums = Album.objects.filter(user=user)

files = list(os.listdir(u'tools/'))
files.remove(u'data_generator.py')
if u'thumb' in files:
    files.remove(u'thumb')

if not os.path.isdir(u'tools/thumb'):
    os.makedirs(u'tools/thumb')

for img in files:
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
    thumb = Image.open('tools/' + img)
    try:
        # Create thumb
        thumb.thumbnail((480, 200), Image.ANTIALIAS)
        thumb.save('tools/thumb/' + img + '.thumbnail', 'JPEG')
        thumb.close()
        # Save thumb
        thumb = File(open('tools/thumb/' + img + '.thumbnail', 'rb'))
        thumb.name = tmp.name
        p.thumb = thumb
        p.origin_thumb = thumb
        p.save()

    except:
        print 'fail'
        continue

    thumb.close()
    tmp.close()
