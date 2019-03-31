import os
import threading

from youtube_dl import YoutubeDL

import utils


class YTDownloadStatus(object):
    def __init__(self):
        self._status = None

    def set_status(self, d):
        self._status = d

    def get_status(self):
        return self._status

    def to_string(self):
        return utils.status_to_string(self._status)


class YTDownloadProcess(object):
    def __init__(self):
        self._statuses = []
        self._lock = threading.Lock()

    def download_music(self, url):
        status = self._append_new_status()
        self._update_status({'status': 'Start', 'url': url}, status)
        with self._prepare_yt_downloader(status) as ytdl:
            ytdl.download([url])
        status_content = status.get_status()
        self._update_status({'status': 'Ended', 'filename': status_content['filename']}, status)

    def _append_new_status(self):
        status = YTDownloadStatus()
        with self._lock:
            self._statuses.append(status)
        return status

    def _prepare_yt_downloader(self, status):
        opts = utils.build_ytopts(
            progress_hooks=[lambda d: self._update_status(d, status)]
        )
        return YoutubeDL(opts)

    def _update_status(self, d, status):
        status.set_status(d)
        self._print_statuses()

    def _print_statuses(self):
        with self._lock:
            statuses_string = list(s.to_string() for s in self._statuses)
            utils.clear_print(os.linesep.join(statuses_string))
