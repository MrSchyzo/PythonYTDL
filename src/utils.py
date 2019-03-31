from optional import Optional


def clear_print(msg):
    clear_sequence = "\033[H\033[J"
    print(clear_sequence + msg)


class YTDLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


def ytdl_hook(d):
    if d['status'] == 'downloading':
        clear_print("%s %s: %s @ %s, eta %s" % (
            d['status'],
            d['filename'],
            d['_percent_str'],
            d['_speed_str'],
            d['_eta_str']
        ))
        pass

    if d['status'] == 'finished':
        clear_print("%s %s: downloaded video %s in %s; now converting to mp3." %(
            d['status'],
            d['filename'],
            d['_total_bytes_str'],
            d['_elapsed_str']
        ))
        pass


def build_ytopts(
        format=None,
        logger=None,
        progress_hooks=None,
        outtmpl=None,
        postprocessors=None
):
    return {
        'format': Optional.of_nullable(format).or_else('bestaudio/best'),
        'logger': Optional.of_nullable(logger).or_else(YTDLogger()),
        'progress_hooks': Optional.of_nullable(progress_hooks).or_else([ytdl_hook]),
        'outtmpl': Optional.of_nullable(outtmpl).or_else('%(title)s.%(ext)s'),
        'postprocessors': Optional.of_nullable(postprocessors).or_else([{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '384',
        }]),
    }
