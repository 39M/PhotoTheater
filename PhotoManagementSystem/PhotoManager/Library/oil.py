from PIL import Image
import numpy as ny
import random


def oil():
    graph = Image.open('../PhotoManager/source.jpg')
    size = graph.size
    width = size[0]
    height = size[1]

    N = 1
    source = ny.array(graph)
    result = source
    for h in range(1 + N, height - N):
        for w in range(1 + N, width - N):
            k1 = random.random() - 0.5
            k2 = random.random() - 0.5
            m = k1 * (N * 2 - 1)
            n = k2 * (N * 2 - 1)
            hnew = int((h + m) % height)
            wnew = int((w + n) % width)
            wnew = width if wnew == 0 else wnew
            hnew = width if hnew == 0 else hnew
            result[h][w] = source[hnew][wnew]

    Image.fromarray(result).save('../PhotoManager/result.jpg')
