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
                if r > border and g > border and b > border:
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
    else:
        return cropPicture4x3(im)

def cropPicture4x3(im):
    height = im.size[1]
    width = im.size[0]
    im1 = im.crop((int(width/10), int(height/20), int(width/2), int(height/5)))
    im2 = im.crop((int(width * 0.6), int(height/10), width, int(height/5)))
    im3 = im.crop((int(width/3), int(height /5), int(width * 2/3), int(height/2)))  # 通常は2/5で良い、ガレージのときは1/2
    im4 = im.crop((int(width * 209/450), 0, int(width * 216/450), int(height * 7/325)))
    im5 = im.crop((int(width * 234/450), 0, int(width * 241/450), int(height * 7/325)))
    im6 = im.crop((int(width * 209/450), 0, int(width * 241/450), int(height * 7/325)))
    return [im1, im2, im3, im4, im5, im6, im, im]

def cropPicture16x9(im):
    height = im.size[1]
    width = im.size[0]

    # プレイヤーリスト、左右
    l = []
    r = []
    up = int(0.15 * height)
    bt = int(0.1875 * height)
    gap = int(0.049 * height)

    '''縮小UIに対応したもの
    map     = im.crop((int(width/4), int(height * 15/80), int(width/2), int(height * 19 / 80)))
    desc    = im.crop((int(width * 23/40), int(height/5), int(width * 4/5), int(height * 9/40)))
    result  = im.crop((int(width * 5/12), int(height/5), int(width * 7/12), int(height * 2/5)))
    hp_l = im.crop((int(width * 0.42), 0, int(width * 0.46), int(height * 0.04)))
    hp_r = im.crop((int(width * 0.54), 0, int(width * 0.58), int(height * 0.04)))
    im6 = im.crop((int(width * 209/450), 0, int(width * 241/450), int(height * 7/325)))
    '''

    map     = im.crop((int(width * 0.18), int(height * 0.13), int(width * 0.4), int(height * 0.18)))
    desc    = im.crop((int(width * 0.6), int(height * 0.14), int(width * 0.86), int(height * 0.175)))
    result  = im.crop((int(width * 5/12), int(height/5), int(width * 7/12), int(height * 2/5)))
    hp_l = im.crop((int(width * 0.29), int(height * 0.01), int(width * 0.457), int(height * 0.035)))
    hp_r = im.crop((int(width * 0.543), int(height * 0.01), int(width * 0.81), int(height * 0.035)))
    im6 = im.crop((int(width * 209/450), 0, int(width * 241/450), int(height * 7/325)))

    for i in range(7):
        l_new = im.crop((int(width * 0.1), up, int(width * 0.13), bt))
        r_new = im.crop((int(width * 0.87), up, int(width * 0.9), bt))
        l.append(l_new)
        r.append(r_new)
        up = up + gap
        bt = bt + gap

    return [map, desc, result, 
            hp_l, hp_r, im6,
            l[0], l[1], l[2], l[3], l[4], l[5], l[6],
            r[0], r[1], r[2], r[3], r[4], r[5], r[6]]