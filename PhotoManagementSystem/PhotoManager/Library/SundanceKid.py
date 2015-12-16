from PIL import Image
import numpy as ny


def sundancekid():
    graph = Image.open('../PhotoManager/source.jpg')

    source = ny.double(ny.array(graph))
    result = source
    for dim in range(3):
        # temp = ny.uint8(source[:, :, dim] * 3 / 255)
        # result[:, :, dim] = 20 * temp * temp + 45 * temp + 42
        temp = ny.uint8(source[:, :, dim] * 2 / 255)
        result[:, :, dim] = 122 * temp + 61

    result = Image.fromarray(ny.uint8(result)).convert('RGB')
    result.save('../PhotoManager/result.jpg')
