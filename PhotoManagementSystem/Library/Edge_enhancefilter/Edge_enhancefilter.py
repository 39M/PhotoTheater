from PIL import Image
import ImageFilter

im = Image.open('source.jpg')
im = im.convert("RGB")
Enhance = im.filter(ImageFilter.EDGE_ENHANCE)
Enhance.save('result.jpg')
