from aeneas.executetask import ExecuteTask
from aeneas.task import Task
from playsound import playsound
from multiprocessing import Process
from spleeter.separator import Separator
import json
import time
import os
import cut_mp3
import string
import re
import urllib.request
from bs4 import BeautifulSoup
import get_images

def youtube_download (url):
    print ("downloading youtube song")
    if (os.path.isfile("music/song_download.mp3")):
        os.remove ("music/song_download.mp3")
    os.system ('youtube-dl -x --audio-format mp3 --no-continue -o "music/song_download.mp3" {}'.format(url))

def split_stems ():
    print ("splitting stems with spleeter")
    separator = Separator("spleeter:2stems")
    if (os.path.isfile ("music\\song_download\\vocals.wav")):
        os.remove ("music\\song_download\\vocals.wav")
    if (os.path.isfile ("music\\song_download\\accompaniment.wav")):
        os.remove ("music\\song_download\\accompaniment.wav")
    if (os.path.isfile ("music\\song_download\\vocals.mp3")):
        os.remove ("music\\song_download\\vocals.mp3")
    separator.separate_to_file('music/song_download.mp3', 'music/')
    os.system ("ffmpeg -y -i music\\song_download\\vocals.wav -b:a 320000 music\\song_download\\vocals.mp3")

def get_lyrics (artist, song_name):
    artist = artist.lower()
    song_title = song_name.lower()
    # remove all except alphanumeric characters from artist and song_title
    artist = re.sub('[^A-Za-z0-9]+', "", artist)
    song_title = re.sub('[^A-Za-z0-9]+', "", song_title)
    if artist.startswith("the"):    # remove starting 'the' from artist e.g. the who -> who
        artist = artist[3:]
    url = "http://azlyrics.com/lyrics/"+artist+"/"+song_title+".html"
    
    try:
        content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(content, 'html.parser')
        lyrics = str(soup)
        # lyrics lies between up_partition and down_partition
        up_partition = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
        down_partition = '<!-- MxM banner -->'
        lyrics = lyrics.split(up_partition)[1]
        lyrics = lyrics.split(down_partition)[0]
        lyrics = lyrics.replace('<br>','').replace('</br>','').replace('<br/>','').replace('</div>','').strip()
        lyrics = lyrics.replace ("\n\n", '\n')
        lyrics = lyrics.replace (",", "")
        lyrics = re.sub(r'[^\x00-\x7F]+','', lyrics)
        with open ("lyrics/song_lyrics.txt", 'w') as f:
            f.write (lyrics)
    except Exception as e:
        return "Exception occurred \n" +str(e)

def lyrics_to_time ():
    # create Task object
    config_string = u"task_language=eng|is_text_type=plain|os_task_file_format=json"
    task = Task(config_string=config_string)
    task.audio_file_path_absolute = u"music/song_download/vocals.mp3"
    task.text_file_path_absolute = u"lyrics/song_lyrics.txt"
    task.sync_map_file_path_absolute = u"aeneas_stuff/song.json"

    # process Task
    ExecuteTask(task).execute()

    # output sync map to file
    task.output_sync_map_file()

def time_words (total):
    # create Task object
    for num in range (total):
        config_string = u"task_language=eng|is_text_type=plain|os_task_file_format=json"
        task = Task(config_string=config_string)
        task.audio_file_path_absolute = u'exports/song_{}-extract.mp3'.format (str(num))
        task.text_file_path_absolute = u'word_times/song_{}-extract.txt'.format (str(num))
        task.sync_map_file_path_absolute = u"AENEAS_STEMS/song_{}.json".format (str(num))
        # process Task
        ExecuteTask(task).execute()
        # output sync map to file
        task.output_sync_map_file()

def combine_stems (total):
    final_json = {}
    final_json ["fragments"] = []
    last_time = 0
    id_num = 0
    for num in range (total):
        current_times = open ("AENEAS_STEMS/song_{}.json".format(num))
        current_times = json.load (current_times)
        for fragment in current_times["fragments"]:
            fragment["end"] = str(float(fragment["end"]) + last_time)
            fragment["begin"] = str(float(fragment["begin"]) + last_time)
            fragment["id"] = "song{}".format (id_num)
            id_num += 1
            final_json ["fragments"].append (fragment)
        last_time = float(fragment["end"])
    with open ("aeneas_stuff/song.json", 'w') as outfile:
        json.dump (final_json, outfile, indent=4)

#lyrics_to_time ()
#time_words ()
# combine_stems ()

# main stuff:
def play_music ():
    song_name = "song"
    playsound ("music/song_download/vocals.mp3")

def print_lyrics ():    
    song_name = "song"
    all_lyrics = open ("aeneas_stuff/{}.json".format(song_name))
    all_lyrics = json.load (all_lyrics)
    for lyric in all_lyrics["fragments"]:
        print (lyric["lines"][0])
        begin_time = float(lyric["begin"])
        end_time = float (lyric["end"])
        time.sleep (end_time-begin_time)

if __name__ == "__main__":
    
    # song_name = "the scotts"
    # artist = "travis scott"
    # url = "https://www.youtube.com/watch?v=sw4r0k8WWqU"
    # get_lyrics (artist, song_name)
    # print ("downloaded lyrics")
    # youtube_download (url)
    # print ("downloaded youtube audio")
    # split_stems ()
    # print ("split song into vocal and accompaniment")
    # lyrics_to_time ()
    # print ("converted lyrics to times")
    # total_num = cut_mp3.cut_mp3 ()
    # print ("cut mp3 into segments")
    # time_words (total_num)
    # print ("mapped words with times")
    # combine_stems (total_num)
    # print ("combined all stems into song.json")
    try:
        get_images.main ()
    except:
        get_images.main ()
    print ("SUCCESSFULLY SCRAPED AND CONVERTED GIFS")
    os.system ("python concat_vids.py")
    print ("FULLY DONE!!!")

    # p2 = Process(target=print_lyrics)
    # p2.start()
    # p1 = Process(target=play_music)
    # p1.start()
    # p1.join()
    # p2.join()







