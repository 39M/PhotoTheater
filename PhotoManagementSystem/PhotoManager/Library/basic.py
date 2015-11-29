from PIL import Image
import ImageFilter


def blur():
    im = Image.open('../PhotoManager/source.jpg')
    im = im.convert("RGB")
    result = im.filter(ImageFilter.BLUR)
    result.save('result.jpg')


def detail():
    im = Image.open('../PhotoManager/source.jpg')
    im = im.convert("RGB")
    result = im.filter(ImageFilter.DETAIL)
    result.save('result.jpg')


def edgeenhance():
    im = Image.open('../PhotoManager/source.jpg')
    im = im.convert("RGB")
    result = im.filter(ImageFilter.EDGE_ENHANCE)
    result.save('result.jpg')


def contour():
    im = Image.open('../PhotoManager/source.jpg')
    im = im.convert("RGB")
    result = im.filter(ImageFilter.CONTOUR)
    result.save('result.jpg')


def emboss():
    im = Image.open('../PhotoManager/source.jpg')
    im = im.convert("RGB")
    result = im.filter(ImageFilter.EMBOSS)
    result.save('result.jpg')


def findedge():
    im = Image.open('../PhotoManager/source.jpg')
    im = im.convert("RGB")
    result = im.filter(ImageFilter.FIND_EDGES)
    result.save('result.jpg')


def smooth():
    im = Image.open('../PhotoManager/source.jpg')
    im = im.convert("RGB")
    result = im.filter(ImageFilter.SMOOTH)
    result.save('result.jpg')


def sharpen():
    im = Image.open('../PhotoManager/source.jpg')
    im = im.convert("RGB")
    result = im.filter(ImageFilter.SHARPEN)
    result.save('result.jpg')
