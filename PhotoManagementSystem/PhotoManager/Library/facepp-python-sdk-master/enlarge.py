from PIL import Image
import numpy as ny
import facepp
import math

# -*- coding: utf-8 -*-

API_KEY = 'e6999ac68d52bfb7ba47e3f2f779a225'
API_SECRET = '8yEc6T_9GCIFQl6UFzl6mJ2jL1YkCFWc'

api = facepp.API(API_KEY, API_SECRET)

IMAGE = '.\source.jpg'

# Detect face in the picture and find out his position and attributes

face = api.detection.detect(img=facepp.File(IMAGE), mode='oneface')

face_id = face['face'][0]['face_id']

land_mark = api.detection.landmark(api_key=API_KEY, api_secret=API_SECRET, face_id=face_id, type='25P')

# Operate area
graph = Image.open('source.jpg')
size = graph.size
width = size[0]
height = size[1]

pIn = ny.array(graph)
ptemp = pIn

cenX = int(land_mark['result'][0]['landmark']['left_eye_bottom']['y'] * height / 100)
cenY = int(land_mark['result'][0]['landmark']['left_eye_bottom']['x'] * width / 100)
left_eye_left_corner = int(land_mark['result'][0]['landmark']['left_eye_left_corner']['x'] * width / 100)
left_eye_right_corner = int(land_mark['result'][0]['landmark']['left_eye_right_corner']['x'] * width / 100)
left_eye_top = int(land_mark['result'][0]['landmark']['left_eye_top']['y'] * height / 100)
left_eye_bottom = int(land_mark['result'][0]['landmark']['left_eye_bottom']['y'] * height / 100)
R = left_eye_right_corner - left_eye_left_corner
# R = left_eye_bottom - left_eye_top
R *= 1.1
theta = math.pi
for k in range(3):
    for x in range(1 - cenX, left_eye_bottom - cenX):
        for y in range(1 - cenY, width - cenY):
            disX = int(1.2 * x)
            disY = int(1.2 * y)

            dis = disX * disX + disY * disY
            r = math.sqrt(dis)
            if r <= R and dis != 0:
                xx = 2 * R * disX * math.acos(math.sqrt(R * R - dis) / R) / (theta * r) + cenX
                yy = 2 * R * disY * math.acos(math.sqrt(R * R - dis) / R) / (theta * r) + cenY

                xx = ny.around(ny.array(xx))
                yy = ny.around(ny.array(yy))
                if width >= yy >= 1 and height >= xx >= 1:
                    ptemp[x + cenX, y + cenY, k] = pIn[xx, yy, k]
            else:
                ptemp[x + cenX, y + cenY, k] = pIn[x + cenX, y + cenY, k]

pOut = ptemp
bias = height / 64
cenX = int(land_mark['result'][0]['landmark']['right_eye_bottom']['y'] * height / 100) + bias
cenY = int(land_mark['result'][0]['landmark']['right_eye_bottom']['x'] * width / 100)
right_eye_left_corner = int(land_mark['result'][0]['landmark']['right_eye_left_corner']['x'] * width / 100)
right_eye_right_corner = int(land_mark['result'][0]['landmark']['right_eye_right_corner']['x'] * width / 100)
right_eye_top = int(land_mark['result'][0]['landmark']['right_eye_top']['y'] * height / 100)
right_eye_bottom = int(land_mark['result'][0]['landmark']['right_eye_bottom']['y'] * height / 100)
R = right_eye_right_corner - right_eye_left_corner
# R = left_eye_bottom - left_eye_top
R *= 1.1
for k in range(3):
    for x in range(1 - cenX, right_eye_bottom + bias - cenX):
        for y in range(1 - cenY, width - cenY):
            disX = int(1.2 * x)
            disY = int(1.2 * y)

            dis = disX * disX + disY * disY
            r = math.sqrt(dis)
            if r <= R and dis != 0:
                xx = 2 * R * disX * math.acos(math.sqrt(R * R - dis) / R) / (theta * r) + cenX
                yy = 2 * R * disY * math.acos(math.sqrt(R * R - dis) / R) / (theta * r) + cenY

                xx = ny.around(ny.array(xx))
                yy = ny.around(ny.array(yy))
                if width >= yy >= 1 and height >= xx >= 1:
                    pOut[x + cenX, y + cenY, k] = pIn[xx, yy, k]
            else:
                pOut[x + cenX, y + cenY, k] = pIn[x + cenX, y + cenY, k]

result = Image.fromarray(ny.uint8(pOut)).convert('RGB')
result.save('result.jpg')
