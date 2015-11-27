from PIL import Image
import ImageFilter

im = Image.open('source.jpg')
im = im.convert("RGB")
blur = im.filter(ImageFilter.BLUR)
blur.save('result.jpg')
