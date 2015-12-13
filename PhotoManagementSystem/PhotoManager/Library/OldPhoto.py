from PIL import Image
import numpy as ny


def oldphoto():
    graph = Image.open('../PhotoManager/source.jpg')
    size = graph.size
    width = size[0]
    height = size[1]

    source = ny.double(ny.array(graph))
    Result = ny.zeros([height, width, 3], dtype=ny.double)
    # Result[:, :] = source[:, :]
    Result[:, :, 0] = 0.393 * source[:, :, 0] + 0.769 * source[:, :, 1] + 0.189 * source[:, :, 2]
    Result[:, :, 1] = 0.349 * source[:, :, 0] + 0.686 * source[:, :, 1] + 0.168 * source[:, :, 2]
    Result[:, :, 2] = 0.272 * source[:, :, 0] + 0.534 * source[:, :, 1] + 0.131 * source[:, :, 2]

    result = Image.fromarray(ny.uint8(Result/1.4)).convert('RGB')
    result.save('../PhotoManager/result.jpg')
