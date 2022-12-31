# 時系列データの処理に関するメソッド
import numpy as np
import pandas as pd
import os
import re
import bisect
import sys
from collections import namedtuple

# ディレクトリdir内にあるlogファイルを統合する
def concateLogs(dir):
    log_list = []
    num_list = []
    for name in os.listdir(dir):
        if(name.startswith('log')):
            num = int(re.search(r'\d+', name).group())
            bisect.insort(num_list, num)
            idx = num_list.index(num)
            log_list.insert(idx, name)
    with open(dir+'/stream.csv', 'w', encoding='utf-8') as new_file:
        for name in log_list:
            with open(dir+'/'+name, 'r') as f:
                for line in f:
                    new_file.write(line)

# 時系列データを非時系列データに変換
def stripTimeStream(inputfile, outputfile, mode='w'):
    # オプションが適切に設定されていないときの例外処理
    if((mode in ['w', 'a']) == False):
        print('Mode must be whether \'w\' or \'a\'.', file=sys.stderr)
    if(os.stat(inputfile).st_size == 0):
        print('Empty input file. stripTimeStream will terminate the process.')
        return

    df = pd.read_csv(inputfile, header=None, names=['time', 'status', 'detail'])
    f = open(outputfile, 'w')
    f.write('map, result, reason\n')    # csvのヘッダ書き出し
    Row = namedtuple('Row', 'status detail')
    last = Row(df.iat[1, 1], df.iat[1, 2])      # 最後の状態、loading, win, loseのいずれかが入る
    for index, data in df.iterrows():
        current = Row(str(data['status']), str(data['detail']))
        if(current.status in ['win', 'lose'] and last.status == 'loading'):
            map = last.detail
            result = current.status
            reason = current.detail
            f.write(map + ',' + result + ',' + reason + '\n')
        last = current