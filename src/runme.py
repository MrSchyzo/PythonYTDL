from __future__ import unicode_literals
from youtube_dl import YoutubeDL as YTDownloader
import utils

songs = [
    'https://www.youtube.com/watch?v=0Bnd_fOmtl0',
    'https://www.youtube.com/watch?v=o_jSN3XwDZs',
    'https://www.youtube.com/watch?v=PVR46Nx_8S8',
    'https://www.youtube.com/watch?v=7jb6huzmTfE',
    'https://www.youtube.com/watch?v=hamKl-su8PE',
    'https://www.youtube.com/watch?v=DN-Dcwq4i2g',
    'https://www.youtube.com/watch?v=l3NoYyNKSXQ',
    'https://www.youtube.com/watch?v=kRDJ5FnxZHg',
]
with YTDownloader(utils.build_ytopts()) as ydl:
    ydl.download(songs)
