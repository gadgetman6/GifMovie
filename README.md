# GifMovie

A fun Python program I made to convert a song into a movie of GIFS synced to the song's lyrics.

Steps (in main.py):
1. Downloads mp3 of song based on name using youtube-dl
2. Scrapes lyrics of song from lyric database (using BeautifulSoup)
3. Uses Deezer Spleeter to split the song into lyrics and instrumental
4. Uses Aeneas to sync words of lyrics with times in song
5. For every unique word in lyrics, scrapes a GIF from Giphy (using Selenium)
6. Uses FFMPEG to convert each GIF to a video file
7. Concatenates all GIF videos, adds original song audio track, and exports to final movie (using FFMPEG)

