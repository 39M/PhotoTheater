from PIL import Image
import numpy as ny
import math


def processing():
    graph = Image.open('../PhotoManager/source.jpg')
    size = graph.size
    width = size[0]
    height = size[1]

    # source = ny.uint16(ny.array(graph))
    result = ny.int32(ny.array(graph))

    rMap = ny.int32(ny.zeros([256]))
    gMap = ny.int32(ny.zeros([256]))
    bMap = ny.int32(ny.zeros([256]))
    for i in range(256):
        value = i if i < 128 else 256 - i
        gray = int(math.pow(value, 3.0) / 64.0 / 256.0)
        rMap[i] = gray if i < 128 else 256 - gray
        gray = int(math.pow(value, 2) / 128.0)
        gMap[i] = gray if i < 128 else 256 - gray
        bMap[i] = i / 2 + 0x25

    for row in range(height):
        for col in range(width):
            b = bMap[result[row, col, 2]]
            g = gMap[result[row, col, 1]]
            r = rMap[result[row, col, 0]]
            b = min(255, max(0, b))
            g = min(255, max(0, g))
            r = min(255, max(0, r))
            result[row, col, 0] = r
            result[row, col, 1] = g
            result[row, col, 2] = b

    result = Image.fromarray(ny.uint8(result)).convert('RGB')
    result.save('../PhotoManager/result.jpg')
