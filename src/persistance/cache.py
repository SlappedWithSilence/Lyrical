import weakref

from loguru import logger

root: list[dict] = []


def initialize_root() -> None:
    """Set up the cache. This should only run once at the start of execution."""

    logger.debug("Initializing cache")

    global root

    root.append({})

    get_cache()["charts"] = {}
    get_cache()["charts"]["yearly"] = {}
    get_cache()["fermented_tracks"] = []
    get_cache()["lyrics"] = {}
    get_cache()["comparisons"] = {}


def set_cache(cache: dict) -> None:
    global root
    root[0] = cache


def get_cache() -> dict:
    global root

    return root[0]


def is_lyric_cached(song):
    """Get cached string containing lyrics for requesting song.

    @:param song
        The song lyrics requested from cache.

    @:returns str
        A string containing the lyrics from the song.

    @:returns None
        Returns None in case of a cache miss.
    """

    global root

    logger.debug(str(get_cache()))
    if song.artist not in get_cache()["lyrics"]:
        return None

    if song.title not in get_cache()["lyrics"][song.artist]:
        return None

    return get_cache()["lyrics"][song.artist][song.title]


def cache_song(song) -> None:
    if not song.lyrics:
        raise ValueError("Cannot cache SongContainer when lyrics=None!")

    get_cache()["lyrics"][song.artist][song.title] = song


def clear_cache() -> None:
    """Delete the contents of the cache."""
    global root

    root = {}


def dump_cache(pickle: bool = True) -> None:
    """
    Write the contents of the cache to disk.

    @:param pickle
        If true, the cache is written as a pickle object. Otherwise, the contents are written in plaintext.

    """
    global root
