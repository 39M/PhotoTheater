from PIL import Image, ImageFilter
import numpy as ny


class MyGaussianBlur(ImageFilter.Filter):
    name = "GaussianBlur"

    def __init__(self, radius=2, bounds=None):
        self.radius = radius
        self.bounds = bounds

    def filter(self, image):
        if self.bounds:
            clips = image.crop(self.bounds).gaussian_blur(self.radius)
            image.paste(clips, self.bounds)
            return image
        else:
            return image.gaussian_blur(self.radius)


def glow():
    graph = Image.open('../PhotoManager/source.jpg')
    size = graph.size
    width = size[0]
    height = size[1]

    source = graph.convert('RGB')
    Gauss = graph.convert('RGB')
    source = ny.double(ny.array(source))

    Gauss = Gauss.filter(MyGaussianBlur(radius=15))
    Gauss = ny.double(ny.array(source))

    Result = ny.zeros([height, width, 3])
    for row in range(height):
        for col in range(width):
            for k in range(3):
                if source[row, col, k] <= 128:
                    value = Gauss[row, col, k] * source[row, col, k] / 128
                    Result[row, col, k] = min(255, max(0, value))
                else:
                    value = 255 - (255 - Gauss[row, col, k]) * (255 - source[row, col, k]) / 128
                    Result[row, col, k] = min(255, max(0, value))

    result = Image.fromarray(ny.uint8(Result)).convert('RGB')
    result.save('../PhotoManager/result.jpg')
