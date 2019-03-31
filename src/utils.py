import math

from optional import Optional


def status_to_string(d):
    if d is None:
        return "Starting..."

    if d['status'] == 'Start':
        return "%s Discovering URL -- %s" % (
            draw_progress(0),
            d['url']
        )

    if d['status'] == 'Ended':
        return "%s Extracted MP3 with success -- %s" % (
            draw_progress(1),
            d['filename']
        )

    if d['status'] == 'downloading':
        cur = d['downloaded_bytes']
        tot = d['total_bytes']
        return ("%s @ %s, eta %s -- %s" % (
            draw_progress(float(cur) / float(tot)),
            d['_speed_str'],
            d['_eta_str'],
            d['filename']
        ))

    if d['status'] == 'finished':
        return ("%s now converting to MP3 -- %s" % (
            draw_progress(1.0),
            d['filename']
        ))

    return "Unknown state!"


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


def draw_progress(zero_to_one_progress=0.0, length=50):
    full_char = u'\u2588'
    quarter_char = u'\u2591'
    half_char = u'\u2592'
    almost_char = u'\u2593'

    progress = length * zero_to_one_progress
    full_char_count = int(math.floor(progress))
    remainder = progress - full_char_count

    next_char = ""
    if remainder > 0.67:
        next_char = almost_char
    elif remainder > 0.33:
        next_char = half_char
    elif remainder > 0.0:
        next_char = quarter_char
    bar_content = ("%s%s%s" % ((full_char * full_char_count), next_char, (" " * length)))[:length]

    return "|%s|" % bar_content


def download_from_queue(queue, downloader):
    while True:
        try:
            url = queue.get()
            downloader.download_music(url)
        except Exception as e:
            print(e.message)
        finally:
            queue.task_done()
