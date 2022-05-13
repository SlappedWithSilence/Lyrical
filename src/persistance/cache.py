import weakref

from src.api.lyrics import SongContainer

root: dict = {}


def initialize_root() -> None:
    """Set up the cache. This should only run once at the start of execution."""
    global root

    root["charts"] = {}
    root["charts"]["yearly"] = {}
    root["fermented_tracks"] = []
    root["lyrics"] = {}
    root["comparisons"] = {}


def get_cache() -> dict:
    """Get a weakref to the cache object.

    @:returns
        Returns a weakref proxy to the cache object. The cache object is a dict.
    """
    global root

    return weakref.proxy(root)


def is_lyric_cached(song: SongContainer) -> [SongContainer, None]:
    """Get cached string containing lyrics for requesting song.

    @:param song
        The song lyrics requested from cache.

    @:returns str
        A string containing the lyrics from the song.

    @:returns None
        Returns None in case of a cache miss.
    """

    global root

    if song.artist not in get_cache()["lyrics"]:
        return None

    if song.title not in get_cache()["lyrics"][song.artist]:
        return None

    return get_cache()["lyrics"][song.artist][song.title]


def cache_song(song: SongContainer) -> None:
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
