from PIL import Image
import numpy as ny
import math


def spin():
    graph = Image.open('../PhotoManager/source.jpg')
    size = graph.size
    width = size[0]
    height = size[1]

    source = ny.array(graph)
    I = ny.double(source)

    Image_new = ny.zeros([height, width, 3])
    Image_new[:] = I[:]
    Center_X = (width + 1) / 2.0
    Center_Y = (height + 1) / 2.0
    validPoint = 1
    angle = 10
    radian = angle * math.pi / 180.0
    radian2 = radian * radian
    Num = 30
    Num2 = Num * Num
    for D in range(3):
        for i in range(height):
            for j in range(width):
                validPoint = 1
                x0 = j - Center_X
                y0 = Center_Y - i
                x1 = x0
                y1 = y0
                Sum_Pixel = I[i, j, D]
                for k in range(Num):
                    x0 = x1
                    y0 = y1
                    x1 = x0 + radian * y0 / Num - radian2 * x0 / Num2
                    y1 = y0 - radian * x0 / Num - radian2 * y0 / Num2
                    x = int(x1 + Center_X)
                    y = int(Center_Y - y1)
                    if 0 < x < width - 1 and 0 < y < height - 1:
                        validPoint += 1
                        Sum_Pixel = Sum_Pixel+I[y, x, D]
                Image_new[i, j, D] = Sum_Pixel / validPoint

    result = Image.fromarray(ny.uint8(Image_new)).convert('RGB')
    result.save('../PhotoManager/result.jpg')
