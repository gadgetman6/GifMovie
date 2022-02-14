from moviepy.editor import *
import json
import string
import os
import numpy as np


final_clips = []

song_name = "toosie"
all_lyrics = open("aeneas_stuff/{}.json".format(song_name))
all_lyrics = json.load(all_lyrics)

num_chunks = 10
lyric_chunks = np.array_split (all_lyrics["fragments"], num_chunks)

chunk_count = 0
num = 0
clips = []

last_time = 0

for chunk in lyric_chunks:
    
    for lyric in chunk:
        word = str(lyric["lines"][0])
        word = word.translate(str.maketrans('', '', string.punctuation))
        word = word.lower()
        if (os.path.isfile("images/{}/{}.gif".format(song_name, word))):
            print (word)
            clip = VideoFileClip ("images/{}/{}.gif".format(song_name, word)).resize(newsize=(1920/2,1080/2))
        else:
            print (word, "IS NOT A FILE")
            clip = VideoFileClip ("images/{}/{}.gif".format(song_name, song_name)).resize(newsize=(1920/2,1080/2))
        begin_time = float(lyric["begin"])
        end_time = float (lyric["end"])
        dur = end_time-begin_time
        #print (dur)
        # if (num==0):
        #     begin_time = float(all_lyrics["fragments"][num+1]["begin"])
        #     end_time = float (all_lyrics["fragments"][num+1]["end"])
        #     durNext = end_time-begin_time
        #     dur += durNext
        clip = clip.fx (vfx.loop, duration=dur)
        clip = clip.set_duration (dur)
        clip = clip.set_start (begin_time)
        clips.append (clip)
        num += 1
            # try:
            #     video = concatenate_videoclips (clips)
            #     print ("Duration:", dur)
            # except:
            #     print ("ERROR-- Duration:", dur, "Clipname:",word)
    chunk_clip = CompositeVideoClip (clips)
    chunk_clip.write_videofile ("temp_files/{}_chunk{}.mp4".format(song_name, chunk_count), codec="mpeg4", preset="ultrafast")
    final_clip = VideoFileClip ("temp_files/{}_chunk{}.mp4".format(song_name, chunk_count))
    if (last_time == 0):
        last_time = final_clip.duration
        final_clips.append (final_clip)
    else:
        final_clip1 = final_clip.subclip(last_time)
        final_clip2 = final_clip1.set_start (last_time)
        last_time = final_clip.duration
        final_clips.append (final_clip2)
    print (last_time)
    final_clips.append (final_clip)
    chunk_count += 1
    for clip in clips:
        clip.close ()

    

video = CompositeVideoClip (final_clips)
audioclip = AudioFileClip ("music/toosie-final.mp3")
video = video.set_audio (audioclip)
#video.preview ()
video.write_videofile ("toosie_gifs_test2.mp4", fps=25, codec="mpeg4", preset="ultrafast")
for clip in final_clips:
    clip.close ()
for chunk in num_chunks:
    os.remove ("temp_files/{}_chunk{}.mp4".format(song_name, chunk))



