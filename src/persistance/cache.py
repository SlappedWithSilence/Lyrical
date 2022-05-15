import pickle
from os import path

from loguru import logger


class Cacher:

    def __init__(self):
        self.__root = None
        self.__initialize_root()

    def __initialize_root(self) -> None:
        """Set up the cache. This should only run once at the start of execution."""

        logger.debug("Initializing cache")

        self.__root = {
            "charts": {
                "yearly": {}
            },
            "fermented_tracks": [],
            "lyrics": {},
            "comparisons": {}
        }

    def set_cache(self, cache: dict) -> None:
        self.__root = cache

    def get_cache(self) -> dict:
        return self.__root

    def is_lyric_cached(self, song):
        """Get cached string containing lyrics for requesting song.

        @:param song
            The song lyrics requested from cache.

        @:returns str
            A string containing the lyrics from the song.

        @:returns None
            Returns None in case of a cache miss.
        """

        if song.artist not in self.__root["lyrics"]:
            return None

        if song.title not in self.__root["lyrics"][song.artist]:
            return None

        return self.__root["lyrics"][song.artist][song.title]

    def cache_song(self, song) -> None:
        if not song.lyrics:
            raise ValueError("Cannot cache SongContainer when lyrics=None!")

        if not song.artist in self.__root["lyrics"]:
            self.__root["lyrics"][song.artist] = {}

        self.__root["lyrics"][song.artist][song.title] = song

    def clear_cache(self) -> None:
        """Delete the contents of the cache."""
        self.__root = {}

    def dump_cache(self, pth: str) -> None:
        """
        Write the contents of the cache to disk.

        @:param pickle
            If true, the cache is written as a pickle object. Otherwise, the contents are written in plaintext.

        """
        with open(pth, "wb") as f:
            pickle.dump(self.__root, f)

    def load_cache(self, pth: str):
        if path.exists(pth):
            # Load
            with open(pth, "r") as f:
                self.set_cache(pickle.load(f))


cache = Cacher()
lyric_fail_count: int = 0
