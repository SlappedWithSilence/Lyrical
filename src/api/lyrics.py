import time
from threading import Lock
from typing import Union

import billboard
import requests
from loguru import logger

import src.persistance.cache
from src.api.model import SongContainer
from src.persistance.cache import cache, lyric_fail_count

# Globals
last_scrape_lock = Lock()
last_scrape = time.time()


class AZLyricRunner:

    def __init__(self):
        self.__endpoint_url: str = "https://www.azlyrics.com/lyrics/{}/{}.html"
        self.__backup_endpoint: str = "http://webcache.googleusercontent.com/search?q=cache:www.azlyrics.com/lyrics/{}/{" \
                                 "}.html "
        self.__retried: bool = False
        self.__retry: bool = False

        self.__fail_limit = 3

    def get(self, song: SongContainer, use_backup: bool = False) -> Union[None, SongContainer]:
        if lyric_fail_count > self.__fail_limit:
            return None

        if not (song.artist and song.title):
            return None

        cache_result = cache.is_lyric_cached(song)

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
            logger.debug(f"Done scraping {song}")

            updated_song_container = song.set_lyrics(lyrics)
            cache.cache_song(updated_song_container)
            logger.debug(f"Done caching {song}")

            return updated_song_container

        except IndexError as e:
            logger.info(f"Failed parse HTML for {str(song)}: {str(e)}")
            logger.debug(e)
            logger.debug(self.__endpoint_url)
            src.persistance.cache.lyric_fail_count = src.persistance.cache.lyric_fail_count + 1
            return song.set_failed(True)


def get_lyrics(song) -> str:
    global last_scrape, last_scrape_lock

    last_scrape_lock.acquire()
    if time.time() - last_scrape < 10:
        time.sleep(time.time() - last_scrape)
        last_scrape = time.time()
    last_scrape_lock.release()

    if isinstance(song, billboard.ChartEntry):
        runner = AZLyricRunner()
        return runner.get(SongContainer(artist=song.artist, title=song.title)).lyrics
