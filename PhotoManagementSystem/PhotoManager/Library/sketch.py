from PIL import Image
import numpy as ny
import math


def sketch():
    graph = Image.open('../PhotoManager/source.jpg')
    size = graph.size
    width = size[0]
    height = size[1]

    source = ny.array(graph)

    N = ny.zeros([height, width])
    g = ny.zeros([height, width])
    imggray = ny.zeros([height, width])
    for i in range(height):
        for j in range(width):
            imggray[i, j] = (source[i, j, 0] * 30 + source[i, j, 1] * 59 + source[i, j, 2] * 11 + 50) / 100
    out = ny.zeros([height, width])

    for i in range(height):
        for j in range(width):
            N[i, j] = 255 - imggray[i, j]

    # Get the Gauss template
    R = 5
    F = ny.zeros([2 * R + 1, 2 * R + 1])
    sigma = R / 3
    r = 0
    K = 0
    for x in range(2 * R + 1):
        for y in range(2 * R + 1):
            r = (x - R) * (x - R) + (y - R) * (y - R)
            F[x, y] = math.exp(-r / (2 * sigma * sigma))
            K = K + F[x, y]

    # Imfilter(N, F) / K
    for i in range(height):
        for j in range(width):
            top = min(height, i + R)
            bottom = max(0, i - R)
            left = max(0, j - R)
            right = min(width, j + R)
            temp = 0
            for x in range(bottom, top):
                for y in range(left, right):
                    temp += F[x - bottom, y - left] * N[x, y]
            g[i, j] = temp / K

    for i in range(height):
        for j in range(width):
            b = float(g[i, j])
            a = float(imggray[i, j])
            temp = a + a * b / (256 - b)
            out[i, j] = int(min(temp, 255))

    result = Image.fromarray(ny.uint8(out)).convert('RGB')
    result.save('../PhotoManager/result.jpg')
