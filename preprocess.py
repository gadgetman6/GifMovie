import os
from spleeter.separator import Separator

def download_song (url):
    os.system ('youtube-dl -x --audio-format mp3 -o "music/song_download.mp3" {}'.format(url))

def split_song ():
    separator = Separator("spleeter:2stems")
    separator.separate_to_file('music/song_download.mp3', 'music/')
    