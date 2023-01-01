from PIL import Image

# pic2bin()で用いるモード
NORMAL_BIN = 0
RED_BLUE = 1

# 画像の二値化関数
def pic2bin(image, border, mode=NORMAL_BIN):
    size = image.size
    image2 = Image.new('RGB', size)
    for x in range(size[0]):
        for y in range(size[1]):
            color = image.getpixel((x, y))
            r = color[0]
            g = color[1]
            b = color[2]
            if mode == NORMAL_BIN:  # ピクセルの輝度を基準に二値化
                if r < border or g < border or b < border:
                    r = g = b = 0
                else:
                    r = g = b = 255
                image2.putpixel((x, y), (r, g, b))
            if mode == RED_BLUE:   # 赤いピクセルを白くして二値化
                if r > 50 or b > 50:
                    r = g = b = 255
                else:
                    r = g = b = 0
                image2.putpixel((x, y), (r, g, b))
    return image2

def cropPicture(im):
    height = im.size[1]
    width = im.size[0]
    aspect = width / height
    if aspect == 16/9:
        return cropPicture16x9(im)
    elif aspect == 4/3:
        return cropPicture4x3(im)

def cropPicture4x3(im):
    height = im.size[1]
    width = im.size[0]
    im1 = im.crop((int(width/10), int(height/20), int(width/2), int(height/5)))
    im2 = im.crop((int(width * 0.6), int(height/10), width, int(height/5)))
    im3 = im.crop((int(width/3), int(height /5), int(width * 2/3), int(height * 2/5)))
    im4 = im.crop((int(width * 209/450), 0, int(width * 216/450), int(height * 7/325)))
    im5 = im.crop((int(width * 234/450), 0, int(width * 241/450), int(height * 7/325)))
    im6 = im.crop((int(width * 209/450), 0, int(width * 241/450), int(height * 7/325)))
    return im1, im2, im3, im4, im5, im6

def cropPicture16x9(im):
    height = im.size[1]
    width = im.size[0]
    im1 = im.crop((int(width/4), int(height * 15/80), int(width/2), int(height * 19 / 80)))
    im2 = im.crop((int(width * 23/40), int(height/5), int(width * 4/5), int(height * 9/40)))
    im3 = im.crop((int(width * 5/12), int(height/5), int(width * 7/12), int(height * 2/5)))
    im4 = im.crop((int(width * 209/450), 0, int(width * 216/450), int(height * 7/325)))
    im5 = im.crop((int(width * 234/450), 0, int(width * 241/450), int(height * 7/325)))
    im6 = im.crop((int(width * 209/450), 0, int(width * 241/450), int(height * 7/325)))
    return im1, im2, im3, im4, im5, im6