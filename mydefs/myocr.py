import pyocr
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
from multiprocessing import Process
import mydefs

# OCRのメイン部分
# 直列・並列にする場合もこのメソッドを呼び出す
# 引数: 画像のnparray、ocrエンジン、ocrビルダー、言語(デフォルト: 日本語)
# 戻り値: 画像から検出されたテキスト
def OCRcore(im, engine, builder, lang="jpn"):
    txt = engine.image_to_string(im, lang=lang)
    return txt

# 外部からOCRを呼び出すときに使うメソッド
# captureVideo()などで使う
def OCRmain(im):
    result_list = ['win,elimination', 'lose,elimination',
                    'win,points', 'lose,points']

    # OCRエンジンを取得
    engines = pyocr.get_available_tools()
    engine = engines[0]

    # OCRエンジンの設定
    builder = pyocr.builders.TextBuilder(tesseract_layout = 5)

    im1, im2, im3 = mydefs.cropPicture4x3(im)
    im1 = mydefs.pic2bin(im1, 200)
    im2 = mydefs.pic2bin(im2, 200)
    im3 = mydefs.pic2bin(im3, 170)
    txt1 = OCRcore(im1, engine, builder, lang='jpn')
    txt2 = OCRcore(im2, engine, builder, lang='jpn')
    txt3 = OCRcore(im3, engine, builder, lang='jpn')
    map = mydefs.ifMap(txt1)
    load = mydefs.ifLoading(txt2)
    result = mydefs.ifResult(txt3)
    if(load != False):
        ret = 'loading,' + map + '\n'
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
def sequentialOCR(dir):
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
        txt1 = OCRcore(im1, engine, builder, lang='jpn')
        txt2 = OCRcore(im2, engine, builder, lang='jpn')
        txt3 = OCRcore(im3, engine, builder, lang='jpn')
        map = mydefs.ifMap(txt1)
        load = mydefs.ifLoading(txt2)
        result = mydefs.ifResult(txt3)
        if(load != False):
            f.write(str(t) + ',' + 'loading,' + map + '\n')
        elif(result != False):
            f.write(str(t) + ',' + result_list[result-1] + '\n')
    f.close()