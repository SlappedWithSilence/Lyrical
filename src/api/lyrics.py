import re
import time
from threading import Lock
from typing import Union

import billboard
import requests
from loguru import logger

from src.persistance.cache import is_lyric_cached, cache_song

# Globals
last_scrape_lock = Lock()
last_scrape = time.time()


class SongContainer:

    def __init__(self, artist: str, title: str) -> None:
        self.lyrics: str = None
        self.failed: bool = False

        self.proper = {"artist": artist, "title": title}

        self.title = re.sub('[^A-Za-z0-9]+', "", title.lower())  # Remove all non-alpha-numeric chars
        self.artist = re.sub('[^A-Za-z0-9]+', "", artist.lower())  # Remove all non-alpha-numeric chars
        if self.artist.startswith("the"):  # Remove "the" from the front of the artist string
            self.artist = self.artist[3:]
        self.artist = self.artist.split("featuring")[0]

    def set_lyrics(self, lyrics: str) -> any:
        self.lyrics = lyrics
        return self

    def set_failed(self, status: bool) -> any:
        self.failed = status
        return self

    def __str__(self) -> str:
        return f"{self.artist} - {self.title}"


class AZLyricRunner:

    def __init__(self):
        self.__endpoint_url = "https://www.azlyrics.com/lyrics/{}/{}.html"
        self.__backup_endpoint = "http://webcache.googleusercontent.com/search?q=cache:www.azlyrics.com/lyrics/{}/{}.html"
        self.__retried = False
        self.__retry = False

    def get(self, song: SongContainer, use_backup: bool = False) -> Union[None, SongContainer]:

        if not (song.artist and song.title):
            return None

        cache_result = is_lyric_cached(song)

        if cache_result:
            return cache_result

        self.__endpoint_url = self.__endpoint_url.format(song.artist, song.title)

        try:
            header = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
                'referer': 'https://www.google.com/'
            }

            content = requests.get(self.__endpoint_url, headers=header)
            lyrics = content.text

            # lyrics are between upper bound and lower_bound
            upper_bound = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
            lower_bound = "<!-- MxM banner -->"

            lyrics = lyrics.split(upper_bound)[1]
            lyrics = lyrics.split(lower_bound)[0]
            lyrics = lyrics.replace('<br>', '').replace('</br>', '').replace('</div>', '').strip()

            updated_song_container = song.set_lyrics(lyrics)
            cache_song(updated_song_container)
            return updated_song_container

        except Exception as e:
            logger.info(f"Failed to look up {str(song)}: {str(e)}")
            logger.debug(self.__endpoint_url)
            return song.set_failed(True)


def get_lyrics(song) -> str:
    global last_scrape, last_scrape_lock

    last_scrape_lock.acquire()
    if time.time() - last_scrape < 1.5:
        time.sleep(time.time() - last_scrape)
        last_scrape = time.time()
    last_scrape_lock.release()

    if isinstance(song, billboard.ChartEntry):
        runner = AZLyricRunner()
        return runner.get(SongContainer(artist=song.artist, title=song.title)).lyrics
