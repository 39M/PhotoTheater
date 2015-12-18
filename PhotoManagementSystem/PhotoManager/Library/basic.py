from PIL import Image
import ImageFilter


def blur(src, dst):
    im = Image.open(src)
    im = im.convert("RGB")
    result = im.filter(ImageFilter.BLUR)
    result.save(dst)


def detail(src, dst):
    im = Image.open(src)
    im = im.convert("RGB")
    result = im.filter(ImageFilter.DETAIL)
    result.save(dst)


def edgeenhance(src, dst):
    im = Image.open(src)
    im = im.convert("RGB")
    result = im.filter(ImageFilter.EDGE_ENHANCE)
    result.save(dst)


def contour(src, dst):
    im = Image.open(src)
    im = im.convert("RGB")
    result = im.filter(ImageFilter.CONTOUR)
    result.save(dst)


def emboss(src, dst):
    im = Image.open(src)
    im = im.convert("RGB")
    result = im.filter(ImageFilter.EMBOSS)
    result.save(dst)


def findedge(src, dst):
    im = Image.open(src)
    im = im.convert("RGB")
    result = im.filter(ImageFilter.FIND_EDGES)
    result.save(dst)


def smooth(src, dst):
    im = Image.open(src)
    im = im.convert("RGB")
    result = im.filter(ImageFilter.SMOOTH)
    result.save(dst)


def sharpen(src, dst):
    im = Image.open(src)
    im = im.convert("RGB")
    result = im.filter(ImageFilter.SHARPEN)
    result.save(dst)
