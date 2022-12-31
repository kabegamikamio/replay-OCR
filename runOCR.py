import mydefs
import os
import pyocr
from multiprocessing import Process

dir = '2022-12-30_15-51-09'

if(__name__ == '__main__'):
    file_count = mydefs.countFiles(dir)
    cpus = os.cpu_count()
    block_size = int(file_count / cpus)
    start = 0
    end = block_size
    process_list = []

    for i in range(cpus-1):
        print("process " + str(i) + " launched")
        process = Process(target=mydefs.slaveOCR, args=(dir, start, end))
        process.start()
        process_list.append(process)
        start = end + 1
        end = end + block_size

    print("process " + str(cpus-1) + " launched")
    process = Process(target=mydefs.slaveOCR, args=(dir, start, file_count))
    process.start()
    process_list.append(process)

    for process in process_list:
        process.join()