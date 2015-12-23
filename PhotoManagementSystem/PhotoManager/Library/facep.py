# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import requests

API_KEY = 'e6999ac68d52bfb7ba47e3f2f779a225'
API_SECRET = '8yEc6T_9GCIFQl6UFzl6mJ2jL1YkCFWc'
API_URL = 'http://apicn.faceplusplus.com'


def detect(path):
    data = {
        'api_key': API_KEY,
        'api_secret': API_SECRET,
    }
    files = {
        'img': open(path, 'rb'),
    }
    r = requests.post(API_URL + '/detection/detect',
                      data=data,
                      files=files)
    try:
        face_id = r.json()["face"][0]["face_id"]
        data = {
        'api_key': API_KEY,
        'api_secret': API_SECRET,
        'face_id': face_id
        }
        result = requests.post(API_URL + '/detection/landmark',
                    data=data)
        return result.json()
    except:
        return -1

# detect(u'source.jpg')
