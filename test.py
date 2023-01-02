import mydefs
import pyocr
import pafy
import cv2
from PIL import Image
import datetime
import os
import matplotlib.pyplot as plt
import numpy as np
import sys

url = "https://youtu.be/5qSo8A-hNKM"
t = 279

# 日付を名前とするディレクトリを作成
dt = datetime.datetime.now()
date = 'OCRtest'
# ディレクトリがまだなければ作る
if (os.path.exists(date) == False):
    print('No directory for ' + date + '. Making the dir...')
    os.mkdir(date)

video = pafy.new(url)
vlen = video.length
best = video.getbest(preftype="mp4")
best_url = best.url

cap = cv2.VideoCapture(best_url)      # キャプチャに動画を読み込み
cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)  # キャプチャするタイムスタンプを指定(msec)
ret, frame = cap.read()
if ret == False:
    print('No frame was captured. Try again or the video has some problems in capturing.', file=sys.stderr)
    sys.exit(1)
im = Image.fromarray(frame)

engines = pyocr.get_available_tools()
engine = engines[0]
builder = pyocr.builders.TextBuilder(tesseract_layout=10)

im1, im2, im3, im4, im5, im6 = mydefs.cropPicture4x3(im)
plt.imshow(im4)
plt.show()
txt1 = mydefs.OCRcore(im4, engine=engine, builder=builder, lang='eng')
txt2 = mydefs.OCRcore(im5, engine=engine, builder=builder, lang='eng')
print(txt1 + ':' + txt2)