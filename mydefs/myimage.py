from PIL import Image

# 画像の二値化関数
def pic2bin(image, border):
    size = image.size
    image2 = Image.new('RGB', size)
    for x in range(size[0]):
        for y in range(size[1]):
            color = image.getpixel((x, y))
            r = color[0]
            g = color[1]
            b = color[2]
            if r < border or g < border or b < border:
                r = g = b = 0
            else:
                r = g = b = 255
            image2.putpixel((x, y), (r, g, b))
    return image2

# 画像の切り抜き
def cropPicture4x3(im):
    height = im.size[1]
    width = im.size[0]
    im1 = im.crop((int(width/10), int(height/20), int(width/2), int(height/5)))
    im2 = im.crop((int(width * 0.6), int(height/10), width, int(height/5)))
    im3 = im.crop((int(width/3), int(height /5), int(width * 2/3), int(height * 2/5)))
    return im1, im2, im3