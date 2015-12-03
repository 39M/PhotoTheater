from PIL import Image
import numpy as ny
import math


def f_color(l, percent, height, width):
    l_sort = ny.zeros([height, width])
    l_sort[:, :] = l[:, :]
    l_sort = l_sort.flatten()
    l_sort.sort()

    l_out = ny.zeros([height, width])
    l_out[:, :] = l[:, :]

    if percent == 0:
        l_min = min(l_sort)
        l_max = max(l_sort)
    else:
        l_min = l_sort[math.floor(height * width * percent)]
        l_max = l_sort[math.floor(height * width * (1 - percent))]

    for i in range(height):
        for j in range(width):
            if l[i, j] < l_min:
                l_out[i, j] = l_min
            elif l[i, j] > l_max:
                l_out[i, j] = 1
            else:
                l_out[i, j] = (l[i, j] - l_min) * (1 - l_min) / (l_max - l_min) + l_min

    return l_out


def autolevel():
    graph = Image.open('../PhotoManager/source.jpg')
    size = graph.size
    width = size[0]
    height = size[1]

    source = ny.array(graph, 'f')
    result = source / 255
    R = result[:, :, 0]
    G = result[:, :, 1]
    B = result[:, :, 2]
    percent = 0.001
    result[:, :, 0] = f_color(R, percent, height, width)
    result[:, :, 1] = f_color(G, percent, height, width)
    result[:, :, 2] = f_color(B, percent, height, width)
    result = ny.uint8(result * 255)

    result = Image.fromarray(result).convert('RGB')
    result.save('result.jpg')
