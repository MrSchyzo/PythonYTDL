from __future__ import unicode_literals
from youtube_dl import YoutubeDL as YTDownloader


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '384',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}
with YTDownloader(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=0Bnd_fOmtl0'])
