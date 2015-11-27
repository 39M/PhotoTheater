from PIL import Image
import ImageFilter

im = Image.open('source.jpg')
im = im.convert("RGB")
Detail = im.filter(ImageFilter.DETAIL)
Detail.save('result.jpg')
