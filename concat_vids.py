import os
import json
import string
from subprocess import Popen, call
import numpy as np

output = []
output_txt = ""
song_name = "song"
all_lyrics = open("aeneas_stuff/{}.json".format(song_name))
all_lyrics = json.load(all_lyrics)
words_to_get = all_lyrics["fragments"]

total_dur = 0

for lyric in words_to_get:
    
    word = str(lyric["lines"][0])
    word = word.translate(str.maketrans('', '', string.punctuation))
    word = word.lower()
    vid_id = lyric["id"]
    duration = float(lyric["end"]) - float(lyric["begin"])
    outpoint = float(lyric["end"])
    if (duration > 0.0):
        total_dur += duration
        output_txt += "file 'videos\{}\{}.mp4'".format (song_name, vid_id) + "\n"
        #output_txt += "duration {}".format (duration) + "\n"
        #output_txt += "outpoint {}".format(outpoint) + "\n"

with open ('text_thing.txt', 'w') as f:
    f.write (output_txt)

# print (total_dur)

# for file in os.listdir ("images\{}".format(song_name)):
#     filepath = os.path.join ("images\{}".format(song_name), file)
#     name = file[:-4]
#     print (name)
#     os.system ('ffmpeg -i {} -c copy -f mpegts intermediates\{}.ts -y'.format(filepath, name))

# for lyric in words_to_get:
    
#     word = str(lyric["lines"][0])
#     word = word.translate(str.maketrans('', '', string.punctuation))
#     word = word.lower()
#     if (os.path.isfile ("intermediates\{}.ts".format(word))):
#         filepath = (word+'.ts')
#         output.append(filepath)
        
# #os.system ('ffmpeg -i "concat:{}" -c copy -bsf:a aac_adtstoasc final_vid.mp4'.format(output))
# os.chdir ("intermediates")
# num_chunks = 1
# output_chunks = np.array_split (output, num_chunks)
# chunkNum = 0
# for chunk in output_chunks:   
#     chunk_thing = '|'.join (chunk)
#     print (chunk_thing)
#     os.system ('ffmpeg -i "concat:{}" -c copy -bsf:a aac_adtstoasc final_chunk{}.mp4'.format(chunk_thing, chunkNum))
#     chunkNum += 1

# for i in range (0, len(words_to_get), 2):
#     lyric = words_to_get[i]
#     word1 = str(lyric["lines"][0])
#     word1 = word1.translate(str.maketrans('', '', string.punctuation))
#     word1 = word1.lower()
#     lyric = words_to_get[i+1]
#     word2 = str(lyric["lines"][0])
#     word2 = word2.translate(str.maketrans('', '', string.punctuation))
#     word2 = word2.lower()
#     os.system ('ffmpeg -i videos\\{}\\{}.mp4 -i videos\\{}\\{}.mp4 -crf 18 -filter_complex "[0:v]scale=1024:576,setdar=16/9[v0]; [1:v]scale=1024:576,setdar=16/9[v1]; [v0][v1]concat=n=2:v=1[v]" -map [v] temp\\im{}.mp4'.format (song_name, word1, song_name, word2, i))



# os.system ("ffmpeg -i final_chunk0.mp4 -i ../music/toosie-final.mp3 -c:v copy -c:a aac ../FINAL.mp4")

# ffmpeg -i videos\toosie\black.mp4 -i videos\toosie\black.mp4 -i videos\toosie\gloves.mp4 -filter_complex "[0:v:0]scale=1920:1080[0];[1:v:0]scale=1920:1080[1];[2:v:0]scale=1920:1080[2];concat=n=3:v=1[outv]" -map "[outv]" quicker_vid.mp4

# ffmpeg -i videos\toosie\black.mp4 -i videos\toosie\leather.mp4 -crf 18 -filter_complex "[0:v]scale=1024:576,setdar=16/9[v0]; [1:v]scale=1024:576,setdar=16/9[v1]; [v0][v1]concat=n=2:v=1[v]" -map [v] final_vid.mp4
# ffmpeg -i videos\toosie\black.mp4 -crf 18 -filter_complex "[0:v]scale=1024:576,setdar=16/9[v0]; [v0]concat=n=1:v=1[v]" -map [v] videos\toosie\black.mp4
# ffmpeg -i text_thing.txt -crf 18 -filter_script filters.txt -map [v] final_vid.mp4

filter_complex = ""
end_thing = ""
paths = ""


new_words = []

for i in range (len(words_to_get)):
    lyric = words_to_get[i]
    duration = float(lyric["end"]) - float(lyric["begin"])
    if (duration > 0.0):
        new_words.append (lyric)

words_to_get = new_words

for i in range (len(words_to_get)):
    lyric = words_to_get[i]
    vid_id = lyric["id"]
    paths += "-i {}.mp4 ".format (vid_id)
    cur_filter = "[{}:v]scale=1024:576,setdar=16/9[v{}];".format (i, i)
    filter_complex += cur_filter
    end_thing += "[v{}]".format(i)

#filter_complex = filter_complex[:-1]
#filter_complex += end_thing
#filter_complex += "concat=n={}:v=1".format (len(words_to_get[:2]))
filter_complex += "[outv]"

with open ("filters.txt", 'w') as f:
    f.write (filter_complex)
with open ("wordslist.txt", 'w') as f:
    f.write (str(words_to_get))

command = 'ffmpeg -y -f concat -safe 0 -i text_thing.txt -crf 18 -c copy no_audio.mp4'
print ((command))
os.system (command)
# for word in words_to_get:
#     print (word["lines"])
#     print (float(word["end"]) - float(word["begin"]))

# ADDS AUDIO
command = "ffmpeg -y -i no_audio.mp4 -i music/song_download.mp3 -c copy -c:a aac -map 0:v:0 -map 1:a:0 SKECHERS_FINAL_GIF_MOVIE.mp4"
os.system (command)