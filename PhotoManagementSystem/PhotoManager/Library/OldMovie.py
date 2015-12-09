from PIL import Image
import numpy as ny
import math


def mode(base, mix):
    base = float(base)
    mix = float(mix)
    if mix > 128:
        res = int(base + (mix + mix - 255.0) * ((math.sqrt(base / 255.0)) * 255.0 - base) / 255.0)
    else:
        res = int(base + (mix + mix - 255.0) * (base - base * base / 255.0) / 255.0)
    return min(255, max(0, res))


def oldmovie():
    graph = Image.open('../PhotoManager/source.jpg')
    mask = Image.open('../PhotoManager/Library/mask.png')
    size = graph.size
    width = size[0]
    height = size[1]

    mask = mask.resize((width, height))
    mask = ny.uint16(ny.array(mask))
    result = ny.uint16(ny.array(graph))

    b = 10
    g = 130
    r = 200
    gray = 0
    for row in range(height):
        for col in range(width):
            gray = (result[row, col, 0] + result[row, col, 1] + result[row, col, 2]) / 3
            b = mode(gray, b)
            g = mode(gray, g)
            r = mode(gray, r)
            result[row, col, 0] = mode(b, mask[row, col, 0])
            result[row, col, 1] = mode(g, mask[row, col, 1])
            result[row, col, 2] = mode(r, mask[row, col, 2])

    result = Image.fromarray(ny.uint8(result)).convert('RGB')
    result.save('../PhotoManager/result.jpg')
