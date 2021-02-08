from imgpy import Img


# Crop image
with Img(fp='train.gif') as im:
    h, w= im.size
    left, top, right, bottom = 60, 0, h-60, w-0
    im.crop(box=(left, top, right, bottom))
    im.load(limit=10, first=False)
    im.save(fp='random.gif')