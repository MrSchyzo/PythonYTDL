from __future__ import unicode_literals

import threading
import argparse
import time
from multiprocessing import JoinableQueue, cpu_count
from status import YTDownloadProcess
from utils import download_from_queue

parser = argparse.ArgumentParser(description='A minimalistic multithreaded MP3 downloader')
parser.add_argument('-l', '--list', nargs='+', metavar='URL', help='URLs (or IDs) from YT to be downloaded')
parser.add_argument('-p', '--parallel', metavar='N', type=int, help='Number of parallel downloads')
args = parser.parse_args()

songs = args.list or [
    'https://www.youtube.com/watch?v=0Bnd_fOmtl0',
    'https://www.youtube.com/watch?v=o_jSN3XwDZs',
    'https://www.youtube.com/watch?v=BJPI597v9Y4',
    'https://www.youtube.com/watch?v=PVR46Nx_8S8',
    'https://www.youtube.com/watch?v=7jb6huzmTfE',
    'https://www.youtube.com/watch?v=hamKl-su8PE',
    'https://www.youtube.com/watch?v=3tAShpPu6K0',
    'https://www.youtube.com/watch?v=DN-Dcwq4i2g',
    'https://www.youtube.com/watch?v=l1J-2nIovYw',
    'https://www.youtube.com/watch?v=2jjzE44I09c',
    'https://www.youtube.com/watch?v=xHj3dJVO-gI',
    'https://www.youtube.com/watch?v=QFzHOfBC5rs',
    'https://www.youtube.com/watch?v=Op9XDgF_jDo',
    'https://www.youtube.com/watch?v=FNMF2cYszOs',
    'https://www.youtube.com/watch?v=Pmnr1-A3sQU',
]

_start = time.time()
ytp = YTDownloadProcess()
url_queue = JoinableQueue()
workers = []
for i in range(cpu_count() if not isinstance(args.threads, int) or args.threads < 1 else args.threads):
    thread = threading.Thread(target=download_from_queue, args=(url_queue, ytp,))
    thread.daemon = True
    thread.start()
    workers.append(thread)

for s in songs:
    url_queue.put(s)

url_queue.join()
print("All %s URL(s) extracted in %ss!" % (len(songs), time.time() - _start))
