from PIL import Image
import numpy as ny
import facepp

# -*- coding: utf-8 -*-


def baozou():
    API_KEY = 'e6999ac68d52bfb7ba47e3f2f779a225'
    API_SECRET = '8yEc6T_9GCIFQl6UFzl6mJ2jL1YkCFWc'

    api = facepp.API(API_KEY, API_SECRET)

    IMAGE = '../PhotoManager/source.jpg'

    # Detect face in the picture and find out his position and attributes

    face = api.detection.detect(img=facepp.File(IMAGE), mode='oneface')

    face_id = face['face'][0]['face_id']

    land_mark = api.detection.landmark(api_key=API_KEY, api_secret=API_SECRET, face_id=face_id)

    # Operate area
    graph = Image.open('../PhotoManager/source.jpg')
    size = graph.size
    width = size[0]
    height = size[1]

    source = ny.array(graph)
    result = ny.matrix(0.3 * source[:, :, 1] + 0.59 * source[:, :, 2] + 0.11 * source[:, :, 2])
    npercent = 2
    # average = 128
    brightness = sum(sum(result).T) / width / height / 128 / 4
    # result += brightness * 0.9
    result /= brightness
    # result = average + (result - average) * npercent
    for x in range(height):
        for y in range(width):
            if result[x, y] > 220:
                result[x, y] *= (result[x, y] * 2.0 / 255)
            result[x, y] = max(0, min(255, result[x, y]))
    result = Image.fromarray(ny.uint8(result)).convert('RGB')

    left_eyebrow_left_corner = int(land_mark['result'][0]['landmark']['left_eyebrow_left_corner']['x'] * width / 100) / 2 * 2
    left_eyebrow_upper_middle = int(land_mark['result'][0]['landmark']['left_eyebrow_upper_middle']['y'] * height / 100 * 0.97) / 2 * 2
    contour_right7x = int(land_mark['result'][0]['landmark']['contour_right7']['x'] * width / 100) / 2 * 2
    contour_right7y = int(land_mark['result'][0]['landmark']['contour_right7']['y'] * height / 100) / 2 * 2

    box = (left_eyebrow_left_corner, left_eyebrow_upper_middle, contour_right7x, contour_right7y)
    result = result.crop(box)
    size = result.size
    width = size[0]
    height = size[1]

    template = Image.open('template.jpg')
    temp = (width + height) * 2
    template = template.resize([temp, temp])
    per = 0.30
    x1 = int(temp / 2 - width / 2) / 2 * 2
    y1 = int(temp * per - height / 2) / 2 * 2
    x2 = int(temp / 2 + width / 2) / 2 * 2
    y2 = int(temp * per + height / 2) / 2 * 2
    tbox = [x1, y1, x2, y2]
    template.paste(result, tbox)

    result = Image.fromarray(ny.uint8(template)).convert('RGB')
    result.save('../PhotoManager/result.jpg')
