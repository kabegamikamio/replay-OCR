import mydefs
import datetime
import os
import pafy
from multiprocessing import Process

url = "https://youtu.be/iUfvSm69Exs"

if(__name__ == '__main__'):
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

  for i in range(cpus-1):
    print("process " + str(i) + " launched")
    process = Process(target=mydefs.captureVideo, args=(best_url, start, end, date))
    process.start()
    process_list.append(process)
    start = end + 1
    end = end + block_size

  print("process " + str(cpus-1) + " launched")
  process = Process(target=mydefs.captureVideo, args=(best_url, start, vlen, date))
  process.start()
  process_list.append(process)
  for process in process_list:
    process.join()