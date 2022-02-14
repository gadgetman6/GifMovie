from pydub import AudioSegment
import json


def cut_mp3 ():
    num = 0
    song_name = "song"
    all_lyrics = open ("aeneas_stuff/{}.json".format(song_name))
    all_lyrics = json.load (all_lyrics)
    for lyric in all_lyrics["fragments"]:
        print (lyric["lines"][0])
        begin_time = float(lyric["begin"])
        end_time = float (lyric["end"])
        # Time to miliseconds
        startTime = begin_time*1000
        endTime = end_time*1000
        with open (('word_times/song_{}-extract.txt'.format(str(num))), 'w') as f:
            f.write (lyric["lines"][0].replace (" ", "\n"))

        # Opening file and extracting segment
        song = AudioSegment.from_mp3( 'music/song_download/vocals.mp3')
        extract = song[startTime:endTime]
        # Saving
        extract.export( 'exports/song_{}-extract.mp3'.format(str(num)), format="mp3")
        num += 1
    return num