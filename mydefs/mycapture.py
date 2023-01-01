import os
import cv2
from PIL import Image
from tqdm import tqdm
from mydefs.myocr import OCRmain

LANG = 'eng'

# CV2のマルチプロセスを無効化
cv2.setNumThreads(0)

# キャプチャの抽出
# 引数: 動画のURL、開始時間、終了時間、日付、PNG書き出し有無
def captureVideo(url, start, end, dir, writeout=True):
    print("\tstart: " + str(start) +", end: " + str(end))
    cap = cv2.VideoCapture(url)            # キャプチャに動画を読み込み
    fps = cap.get(cv2.CAP_PROP_FPS)             # 動画FPSの取得
    if writeout == False:    # PNG書き出しが無効の場合はログファイルに書き出す
        log_name = 'log-' + str(start) + '-' + str(end)
        log_name = os.path.join(dir, log_name)
        f = open(log_name, 'w')

    # for t in tqdm.tqdm(range(start, end)):
    for t in tqdm(range(start, end+1)):
        ret,frame = cap.read()    # フレームを取得, numpy.ndarray

        # grabでフレームを読み飛ばす、setを使うと遅くなる
        for i in range(int(fps)-1):
            ret = cap.grab()

        outfile = os.path.join(dir, str(t) + '.png')
        if ret == True:
            if writeout == True:
                cv2.imwrite(outfile, frame) # PNGに書き出し
            else:
                im = Image.fromarray(frame)
                buf = OCRmain(im)
                if buf != False:
                    f.write(str(t) + ',' + buf)
        # 終了判定?
        if cv2.waitKey(20) & 0xFF == ord('q'):
                break
    # ログファイルを閉じる
    if writeout == False:
        f.close()
    # 動画を閉じる
    cap.release()