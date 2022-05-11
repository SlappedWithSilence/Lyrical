import weakref

root: dict = {}


def initialize_root() -> None:
    """Set up the cache. This should only run once at the start of execution."""
    global root

    root["charts"] = {}
    root["fermented_tracks"] = []
    root["comparisons"] = {}


def get_cache() -> dict:
    """Get a weakref to the cache object.

    @:returns
        Returns a weakref proxy to the cache object. The cache object is a dict.
    """
    global root

    return weakref.proxy(root)


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
