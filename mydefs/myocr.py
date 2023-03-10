import pyocr
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
from multiprocessing import Process
import mydefs
import re
import cv2

# OCRのメイン部分
# 直列・並列にする場合もこのメソッドを呼び出す
# 引数: 画像のnparray、ocrエンジン、ocrビルダー、言語(デフォルト: 英語)
# 戻り値: 画像から検出されたテキスト
def OCRcore(im, engine, builder, lang='eng'):
    txt = engine.image_to_string(im, builder=builder, lang=lang)
    return txt

# 外部からOCRを呼び出すときに使うメソッド
# captureVideo()などで使う
def OCRmain(im, lang='eng'):
    result_list = ['win,elimination', 'lose,elimination',
                    'win,points', 'lose,points']

    # OCRエンジンを取得
    engines = pyocr.get_available_tools()
    engine = engines[0]

    # OCRエンジンの設定
    builder = pyocr.builders.TextBuilder(tesseract_layout = 3)
    builder2 = pyocr.builders.DigitBuilder()

    ims = mydefs.cropPicture(im)
    ims[0] = mydefs.pic2bin(ims[0], 195)
    ims[1] = mydefs.pic2bin(ims[1], 200)
    ims[2] = mydefs.pic2bin(ims[2], 170)
    ims[3] = mydefs.pic2bin(ims[3], 180)
    ims[4] = mydefs.pic2bin(ims[4], 180)
    plt.imshow(ims[3])
    plt.show()

    '''
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.imshow(ims[3])
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.imshow(ims[4])
    plt.show()
    '''

    txt_l = []
    txt_r = []

    txt1 = OCRcore(ims[0], engine, builder, lang=lang)
    txt2 = OCRcore(ims[1], engine, builder, lang=lang)
    txt3 = OCRcore(ims[2], engine, builder, lang=lang)
    txt4 = OCRcore(ims[3], engine, builder, lang='eng')
    txt5 = OCRcore(ims[4], engine, builder, lang='eng')
    print(txt5)

    flag_l, score_l = mydefs.ifScore(txt4)
    flag_r, score_r = mydefs.ifScore(txt5)

    if flag_l == True and flag_r == True:
        print('Score: {} vs {}'.format(score_l, score_r))
        if score_l == 0:
            print('Left lose')
        elif score_r == 0:
            print('Right lose')

    '''
    for i in range(7):
        im_l = mydefs.pic2bin(ims[6+i], 220, mydefs.RED_BLUE)
        # cv_l = np.array(ims[6+i], dtype=np.uint8)
        # cv_l = cv2.cvtColor(cv_l, cv2.COLOR_RGB2BGR)
        im_r = mydefs.pic2bin(ims[13+i], 220, mydefs.RED_BLUE)
        # im_l = cv2.adaptiveThreshold(cv_l, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 51, 20)
        l = OCRcore(im_l, engine, builder2, lang='eng')
        r = OCRcore(im_r, engine, builder2, lang='eng')
        # plt.imshow(im_r)
        # plt.show()
        l = str.replace(l, '\n', '')
        r = str.replace(r, '\n', '')
        l = re.sub(r"\D", "", l)
        r = re.sub(r"\D", "", r)
        if len(l) != 0:
            txt_l.append(int(l))
        if len(r) != 0:
            txt_r.append(int(r))

    if len(txt_l) != 0 and len(txt_r) != 0:
        print(txt_l)
        print(txt_r)
        if len(txt_l) == 0:
            print('left lose')
        elif len(txt_r) == 0:
            print('right lose')
    '''

    map = mydefs.ifMap(txt1, lang)
    print(txt1)
    load = mydefs.ifLoading(txt2, lang)
    result = mydefs.ifResult(txt3, lang)
    if(load != False):
        ret = 'loading,' + map if map != False else 'unknown' + '\n'
        return ret
    elif(result != False):
        ret = result_list[result-1] + '\n'
        return ret
    else:
        return False

# ディレクトリ内のPNGファイル数をカウントする関数
def countFiles(dir):
    count = 0
    for file in os.listdir(dir):
        if '.png' in file:
            count = count + 1
    return count

# OCRを直列に実行
def sequentialOCR(dir, lang='eng'):
    result_list = ['win,elimination', 'lose,elimination',
                    'win,points', 'lose,points']

    log_name = os.path.join(dir, 'log')
    f = open(log_name, 'w')

    # OCRエンジンを取得
    engines = pyocr.get_available_tools()
    engine = engines[0]

    # OCRエンジンの設定
    builder = pyocr.builders.TextBuilder(tesseract_layout = 5)

    # ディレクトリ内のファイル数をカウント
    file_count = countFiles(dir)

    # dir\t.png が存在するときループ
    for t in tqdm(range(file_count)):
        path = os.path.join(dir, str(t) + '.png')   # パスの指定
        im = Image.open(path)
        im1, im2, im3 = mydefs.cropPicture4x3(im)
        im1 = mydefs.pic2bin(im1, 190)
        im2 = mydefs.pic2bin(im2, 220)
        im3 = mydefs.pic2bin(im3, 170)
        txt1 = OCRcore(im1, engine, builder, lang=lang)
        txt2 = OCRcore(im2, engine, builder, lang=lang)
        txt3 = OCRcore(im3, engine, builder, lang=lang)
        map = mydefs.ifMap(txt1)
        load = mydefs.ifLoading(txt2)
        result = mydefs.ifResult(txt3)
        if(load != False):
            f.write(str(t) + ',' + 'loading,' + map + '\n')
        elif(result != False):
            f.write(str(t) + ',' + result_list[result-1] + '\n')
    f.close()