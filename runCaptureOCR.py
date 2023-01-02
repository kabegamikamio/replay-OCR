# キャプチャ、OCR、ストリーム処理を一括実行
import mydefs
import datetime
import os
import sys
from yt_dlp import YoutubeDL
from multiprocessing import Process

# 利用可能な言語リスト
lang_list = ['jpn', 'eng']

if(__name__ == '__main__'):
    url = sys.argv[1]
    lang = sys.argv[2]

    if url == '':
        print('Capturer requires the URL to a video.')
        sys.exit(1)
    if (lang in lang_list) == False:
        print('Illegal language {}. Language must be within followings.'.format(lang))
        print(lang_list)
        sys.exit(1)

    mydefs.LANG = lang

    print('Parallelly capturing the video from ' + url)

    # 日付を名前とするディレクトリを作成
    dt = datetime.datetime.now()
    date = dt.strftime('%Y-%m-%d_%H-%M-%S')
    # ディレクトリがまだなければ作る
    if (os.path.exists(date) == False):
        print('No directory for ' + date + '. Making the dir...')
        os.mkdir(date)

    print('Retrieving video info...')

    ydl_opt = {
        'format': 'best',
        'skip_download': True
    }

    with YoutubeDL(ydl_opt) as ydl:
        info = ydl.extract_info(url, download=False)
        best_url = info['url']
        vlen = info['duration']

    print(best_url)
    if len(best_url) == 0:
        print('No available option for this video.', file=sys.stderr)
        sys.exit(1)
    print('Done.')

    print('initializing multiprocessing...')
    process_list = []
    cpus = os.cpu_count()
    block_size = int(vlen / (cpus-1))
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

    print("process " + str(cpus-2) + " launched")
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