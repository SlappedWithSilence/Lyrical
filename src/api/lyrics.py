import re
from typing import Union

import requests
from bs4 import BeautifulSoup
from loguru import logger


class SongContainer:

    def __init__(self, artist: str, title: str) -> None:
        self.lyrics: str = None
        self.failed: bool = False

        self.title = re.sub('[^A-Za-z0-9]+', "", title.lower())  # Remove all non-alpha-numeric chars
        self.artist = re.sub('[^A-Za-z0-9]+', "", artist.lower())  # Remove all non-alpha-numeric chars
        if self.artist.startswith("the"):  # Remove "the" from the front of the artist string
            self.artist = self.artist[3:]

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

    def get(self, song: SongContainer) -> Union[None, SongContainer, str]:

        if not (song.artist and song.title):
            return None

        self.__endpoint_url = self.__endpoint_url.format(song.artist, song.title)

        try:
            content = requests.get(self.__endpoint_url)
            lyrics = content.text

            # lyrics are between upper bound and lower_bound
            upper_bound = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
            lower_bound = "<!-- MxM banner -->"

            lyrics = lyrics.split(upper_bound)[1]
            lyrics = lyrics.split(lower_bound)[0]
            lyrics = lyrics.replace('<br>', '').replace('</br>', '').replace('</div>', '').strip()
            return song.set_lyrics(lyrics)

        except Exception as e:
            logger.info(f"Failed to look up {str(song)}: {str(e)}")
            return song.set_failed(True)
