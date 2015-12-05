from PIL import Image
import numpy as ny


def blackwhite():
    graph = Image.open('../PhotoManager/source.jpg')
    size = graph.size
    width = size[0]
    height = size[1]
    max_dic = {0: 1.16, 1: 1.25, 2: 0.21}
    max_mid = [
        {1: 1.16, 2: 0.47}, {0: 1.16, 2: -0.25}, {0: 0.47, 1: -0.25}
    ]

    source = ny.double(ny.array(graph))
    result = ny.uint8(ny.zeros([height, width]))
    for row in range(height):
        for col in range(width):
            index = ny.argsort(source[row, col])
            x = source[row, col, index[2]]
            d = source[row, col, index[1]]
            n = source[row, col, index[0]]
            xd = x - d
            dn = d - n
            result[row, col] = max(0, min(255, xd * max_dic[index[2]] + dn * max_mid[index[1]][index[2]] + n))

    result = Image.fromarray(result).convert('RGB')
    result.save('../PhotoManager/result.jpg')
