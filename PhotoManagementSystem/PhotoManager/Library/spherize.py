from PIL import Image
import numpy as ny
import math


def spherize():
    graph = Image.open('../PhotoManager/source.jpg')
    size = graph.size
    width = size[0]
    height = size[1]

    pIn = ny.array(graph)
    pOut = ny.array(graph)
    cenY = height / 2
    cenX = width / 2
    offsetX = 0
    offsetY = 0
    newX = 0
    newY = 0
    radian = 0.0
    for row in range(height):
        for col in range(width):
            offsetX = col - cenX
            offsetY = row - cenY
            radian = math.atan2(offsetY, offsetX)
            radius = int((offsetX * offsetX + offsetY * offsetY) / max(cenX, cenY))
            newX = int(radius * math.cos(radian)) + cenX
            newY = int(radius * math.sin(radian)) + cenY
            newX = min(width - 1, max(0, newX))
            newY = min(height - 1, max(0, newY))
            pOut[row, col, 0] = pIn[newY, newX, 0]
            pOut[row, col, 1] = pIn[newY, newX, 1]
            pOut[row, col, 2] = pIn[newY, newX, 2]

    result = Image.fromarray(ny.uint8(pOut)).convert('RGB')
    result.save('../PhotoManager/result.jpg')
