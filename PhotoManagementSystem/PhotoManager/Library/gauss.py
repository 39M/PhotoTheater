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


def gauss():
    graph = Image.open('../PhotoManager/source.jpg')
    size = graph.size
    width = size[0]
    height = size[1]

    gaussin = graph.convert('RGB')

    gaussin = gaussin.filter(MyGaussianBlur(radius=width * height / 52 / 67))

    result = Image.fromarray(ny.uint8(gaussin)).convert('RGB')
    result.save('result.jpg')
