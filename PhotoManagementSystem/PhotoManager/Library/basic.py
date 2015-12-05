from PIL import Image
import ImageFilter


def blur():
    im = Image.open('../PhotoManager/source.jpg')
    im = im.convert("RGB")
    result = im.filter(ImageFilter.BLUR)
    result.save('../PhotoManager/result.jpg')


def detail():
    im = Image.open('../PhotoManager/source.jpg')
    im = im.convert("RGB")
    result = im.filter(ImageFilter.DETAIL)
    result.save('../PhotoManager/result.jpg')


def edgeenhance():
    im = Image.open('../PhotoManager/source.jpg')
    im = im.convert("RGB")
    result = im.filter(ImageFilter.EDGE_ENHANCE)
    result.save('../PhotoManager/result.jpg')


def contour():
    im = Image.open('../PhotoManager/source.jpg')
    im = im.convert("RGB")
    result = im.filter(ImageFilter.CONTOUR)
    result.save('../PhotoManager/result.jpg')


def emboss():
    im = Image.open('../PhotoManager/source.jpg')
    im = im.convert("RGB")
    result = im.filter(ImageFilter.EMBOSS)
    result.save('../PhotoManager/result.jpg')


def findedge():
    im = Image.open('../PhotoManager/source.jpg')
    im = im.convert("RGB")
    result = im.filter(ImageFilter.FIND_EDGES)
    result.save('../PhotoManager/result.jpg')


def smooth():
    im = Image.open('../PhotoManager/source.jpg')
    im = im.convert("RGB")
    result = im.filter(ImageFilter.SMOOTH)
    result.save('../PhotoManager/result.jpg')


def sharpen():
    im = Image.open('../PhotoManager/source.jpg')
    im = im.convert("RGB")
    result = im.filter(ImageFilter.SHARPEN)
    result.save('../PhotoManager/result.jpg')
