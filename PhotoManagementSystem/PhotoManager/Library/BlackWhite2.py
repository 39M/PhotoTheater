from PIL import Image
import numpy as ny


def blackwhite2():
    graph = Image.open('../PhotoManager/source.jpg')
    size = graph.size
    width = size[0]
    height = size[1]

    source = ny.array(graph)
    red = ny.matrix(ny.double(source[:, :, 0]))
    green = ny.matrix(ny.double(source[:, :, 1]))
    blue = ny.matrix(ny.double(source[:, :, 2]))
    # R = sum(sum(red).T) * 1.0 / width / height
    # red /= R
    result = ny.matrix(0.3 * red + 0.59 * green + 0.11 * blue)
    npercent = 1.5
    brightness = sum(sum(result).T) / width / height / 128
    result /= brightness
    result = brightness + (result - brightness) * npercent
    temp = 0.5 * red / ((green + blue + 1) / 2)
    # result *= temp
    for x in range(height):
        for y in range(width):
            result[x, y] *= temp[x, y]
            # result[x, y] *= (red[x, y] * 1.5)
            # if result[x, y] > 30:
            #     result[x, y] *= (result[x, y] * 4.0 / 255)
            # else:
            #     result[x, y] *= (result[x, y] * 2.0 / 255)
            result[x, y] = max(0, min(255, result[x, y]))

    result = Image.fromarray(ny.uint8(result)).convert('RGB')
    result.save('../PhotoManager/result.jpg')
