from srt import compose, Subtitle
import json
from datetime import timedelta

subs = []

song_name = "toosie"
all_lyrics = open ("aeneas_stuff/{}.json".format(song_name))
all_lyrics = json.load (all_lyrics)
num = 0
for lyric in all_lyrics["fragments"]:
    begin_time = timedelta(seconds=float(lyric["begin"]))
    end_time = timedelta(seconds=float (lyric["end"]))
    subs.append (Subtitle (index=num, start=begin_time, end=end_time, content=lyric["lines"][0]))
    num += 1

with open ("{}.srt".format(song_name), 'w') as f:
    f.write (compose(subs))
    