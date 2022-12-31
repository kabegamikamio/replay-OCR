# キャプチャ、OCR、ストリーム処理を一括実行
import mydefs
import datetime
import os
import sys
import pafy
from multiprocessing import Process

if(__name__ == '__main__'):
    url = sys.argv[1] 
    if url == '':
        print('Capturer requires the URL to a video.')
        sys.exit(1)
    print('Parallelly capturing the video from ' + url)

    # 日付を名前とするディレクトリを作成
    dt = datetime.datetime.now()
    date = dt.strftime('%Y-%m-%d_%H-%M-%S')
    # ディレクトリがまだなければ作る
    if (os.path.exists(date) == False):
        print('No directory for ' + date + '. Making the dir...')
        os.mkdir(date)

    print('Retrieving video info...')
    video = pafy.new(url)
    vlen = video.length
    best = video.getbest(preftype="mp4")
    best_url = best.url
    print('Done.')

    print('initializing multiprocessing...')
    process_list = []
    cpus = os.cpu_count()
    block_size = int(vlen / cpus)
    start = 0
    end = block_size

    print("cpus: " + str(cpus))

    for i in range(cpus-2):
        print("process " + str(i) + " launched")
        process = Process(target=mydefs.captureVideo, args=(best_url, start, end, date, False))
        process.start()
        process_list.append(process)
        start = end + 1
        end = end + block_size

    print("process " + str(cpus-1) + " launched")
    process = Process(target=mydefs.captureVideo, args=(best_url, start, vlen, date, False))
    process.start()
    process_list.append(process)
    for process in process_list:
        process.join()

    # ストリームデータの処理
    input = os.path.join(date, 'stream.csv')
    output = os.path.join(date, 'summary.csv')
    mydefs.concateLogs(date)
    mydefs.stripTimeStream(input, output)