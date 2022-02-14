# Importing Necessary Modules
import requests  # to get image from the web
import shutil  # to save it locally
import json
from bs4 import BeautifulSoup
import imageio
import os, sys
import string
import asyncio
from concurrent.futures import ThreadPoolExecutor
import numpy as np

words_done = []
files_to_remove = []
start = """if (Giphy.renderSearch) {
            Giphy.renderSearch(document.getElementById('react-target'), {
                gifs: """
end = """,
                showTV: """

def fetch (song_name, data):
    num = 0
    data = data[0]
    global words_done
    global files_to_remove
    for lyric in data:
        #print (lyric)
        word = str(lyric["lines"][0])
        word = word.translate(str.maketrans('', '', string.punctuation))
        word = word.lower()
        if (word not in words_done):
            # urlsearch = "https://www.google.com/search?tbm=isch&q={}".format(word)
            # print (urlsearch)
            # response = requests.get (urlsearch)
            # soup = bs4.BeautifulSoup (response.text, "html.parser")
            # image_divs = soup.find_all ("img", class_="rg_i Q4LuWd tx8vtf")
            # print (image_divs)

            # data = json.loads (response.text)
            # print (word)
            # url = (data["hits"][0]["previewURL"])
            filename = "images/{}/{}.gif".format(song_name, word)

            if (not os.path.isfile(filename)):
                print (word)
                # try:
                url = "https://giphy.com/search/{}".format(word)

                data = requests.get(url)
                try:
                    soup = BeautifulSoup(data.text, "html.parser")
                    f = open ('black.html', 'w')
                    f.write (soup.prettify())
                    script = str(soup.find_all("script")[13])
                    d = json.loads((script.split(start))[1].split(end)[0])
                    url = d[0]['images']['source']['url']
                    left, bracket, rest = url.partition("//")
                    block, bracket, right = rest.partition(".")
                    new_url = left + "//" + "i" + "." + right
                except:
                    new_url = "https://i.giphy.com/media/SggILpMXO7Xt6/giphy.gif?cid=ecf05e47c5cb877e9275895f0ea83117c5893e79026bb7e2&rid=giphy.gif"
                print (new_url)
                # Open the url image, set stream to True, this will return the stream content.
                r = requests.get(new_url, stream=True)
                

                # Check if the image was retrieved successfully
                if r.status_code == 200:
                        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                        r.raw.decode_content = True
                        # Open a local file with wb ( write binary ) permission.
                        ext = new_url[-3:]
                        if (ext != "gif"):
                            old_filename = "images/{}/{}.{}".format(song_name, word, ext)
                            new_filename = "images/{}/{}.gif".format(song_name, word)
                            with open(old_filename, 'wb') as f:
                                shutil.copyfileobj(r.raw, f)
                            print ("converting")
                            reader = imageio.get_reader(old_filename)
                            fps = reader.get_meta_data()['fps']

                            writer = imageio.get_writer(new_filename, fps=fps)
                            for i,im in enumerate(reader):
                                sys.stdout.write("\rframe {0}".format(i))
                                sys.stdout.flush()
                                writer.append_data(im)
                            writer.close()
                            files_to_remove.append (old_filename)
                            print("\nSuccessfuly downloaded and converted.")
                        else:
                            with open(filename, 'wb') as f:
                                shutil.copyfileobj(r.raw, f)
                            print('Image sucessfully Downloaded: ', filename)
                else:
                    print('Image Couldn\'t be retreived')
                words_done.append (word)
                num += 1
            
            # check_file = 'videos/{}/{}.mp4'.format(song_name, word)
            # if (not os.path.isfile (check_file)):
            #     print (check_file)
            #     duration = float (lyric["end"]) - float(lyric["begin"])
            #     commands = ['ffmpeg', '-stream_loop -1', '-i images\{}\{}.gif'.format(song_name, word), '-t {}'.format(duration), '-c:v libx264', '-crf 18', '-vf "pad=ceil(iw/2)*2:ceil(ih/2)*2"', "-preset medium",  'videos\{}\{}.mp4'.format(song_name, word), '-y']
            #     # subprocess.Popen (['ffmpeg', '-stream_loop -1', '-i images/{}/{}.gif'.format(song_name, word), '-t {}'.format(duration), '-pix_fmt yub420p', '-vf "scale=trunc(iw/2)*2:trunc(ih/2)*2"', 'images/{}/{}.mp4'.format(song_name, word), '-y'], shell=True)
            #     enter_command = ' '.join (commands)
            #     #print (enter_command)
            #     os.system (enter_command)

def convert_to_mp4 (song_name, data):
    global words_done
    global files_to_remove
    data = data[0]
    for lyric in data:
        #print (lyric)
        word = str(lyric["lines"][0])
        word = word.translate(str.maketrans('', '', string.punctuation))
        word = word.lower()
        print (word)
        check_file = 'videos/{}/{}.mp4'.format(song_name, word)
        if (not os.path.isfile (check_file)):
            print (check_file)
            duration = float (lyric["end"]) - float(lyric["begin"])
            if (duration > 0.0):
                gif_id = lyric["id"]
                commands = ['ffmpeg', '-stream_loop -1', '-i images\{}\{}.gif'.format(song_name, word), '-t {}'.format(duration), '-c:v libx264', '-crf 18', '-filter:v "pad=ceil(iw/2)*2:ceil(ih/2)*2,fps=15,scale=1024:576,setdar=16/9"', "-video_track_timescale 90000", "-preset medium",  'videos\{}\{}.mp4'.format(song_name, gif_id), '-y']
                # subprocess.Popen (['ffmpeg', '-stream_loop -1', '-i images/{}/{}.gif'.format(song_name, word), '-t {}'.format(duration), '-pix_fmt yub420p', '-vf "scale=trunc(iw/2)*2:trunc(ih/2)*2"', 'images/{}/{}.mp4'.format(song_name, word), '-y'], shell=True)
                enter_command = ' '.join (commands)
                #print (enter_command)
                os.system (enter_command)


async def get_images_asynchronous ():
    song_name = "song"
    all_lyrics = open("aeneas_stuff/{}.json".format(song_name))
    all_lyrics = json.load(all_lyrics)
    words_to_get = all_lyrics["fragments"]
    num_workers = 10
    word_chunks = np.array_split (words_to_get, num_workers)
    if (not os.path.exists ("images/song")):
        os.mkdir ("images/song")
    if (not os.path.exists ("videos/song")):
        os.mkdir ("videos/song")
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        loop = asyncio.get_event_loop()
        tasks = [
                loop.run_in_executor(
                    executor,
                    fetch,
                    *(song_name, [chunk])
                     # Allows us to pass in multiple arguments to `fetch`
                )
                
                for chunk in word_chunks
        ]
            
        # Initializes the tasks to run and awaits their results
        for response in await asyncio.gather(*tasks):
            pass

async def converter ():
    song_name = "song"
    all_lyrics = open("aeneas_stuff/{}.json".format(song_name))
    all_lyrics = json.load(all_lyrics)
    words_to_get = all_lyrics["fragments"]
    num_workers = 10
    word_chunks = np.array_split (words_to_get, num_workers)
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        loop = asyncio.get_event_loop()
        tasks = [
                loop.run_in_executor(
                    executor,
                    convert_to_mp4,
                    *(song_name, [chunk])       # Allows us to pass in multiple arguments to `fetch`
                )
                
                for chunk in word_chunks
        ]
            
        # Initializes the tasks to run and awaits their results
        for response in await asyncio.gather(*tasks):
            pass
    


def remove_files (song_name):
    for file in os.listdir ("images/{}".format(song_name)):
        if (not file.endswith(".gif")):
            filepath = os.path.join ("images/{}".format(song_name), file)
            os.remove (filepath)

def main():
    song_name = "song"
    all_lyrics = open("aeneas_stuff/{}.json".format(song_name))
    all_lyrics = json.load(all_lyrics)
    words_to_get = all_lyrics["fragments"]
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_images_asynchronous())
    loop.run_until_complete(future)
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(converter())
    loop.run_until_complete(future)
    print ("DONE! REMOVING FILES")
    remove_files (song_name)