import mydefs
import os

dir = '2022-12-30_15-51-09'

input = os.path.join(dir, 'stream.csv')
output = os.path.join(dir, 'summary.csv')

mydefs.concateLogs(dir)
mydefs.stripTimeStream(input, output)