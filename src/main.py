from multiprocessing.dummy import Pool as ThreadPool
from os import path

from loguru import logger

from api.lyrics import get_lyrics, SongContainer
from api.billboard import BillboardRunner
from persistance.cache import cache

cache_path = "cache.pickle"


def __setup():
    """Perform system setup functions"""

    if path.exists(cache_path):
        cache.load_cache(cache_path)

    logger.debug(str(cache.get_cache()))


def __interpret():
    """Generate a list of content to gather from user input"""
    logger.debug(str(cache.get_cache()))


def __gather(years: list[int], songs: list[SongContainer]) -> None:
    logger.debug(str(cache.get_cache()))
    """Gather requested content from third-party sources"""
    # Set up runners
    runner = BillboardRunner()

    # Get charts
    for year in years:
        if year not in cache.get_cache()["charts"]["yearly"]:
            songs = runner.get(year=year)
            cache.get_cache()["charts"]["yearly"][year] = songs

    # Get lyrics
    worker_pool = ThreadPool(1)

    logger.debug(str(cache.get_cache()))
    for song in songs:
        get_lyrics(song)

    lyrics = worker_pool.map(get_lyrics, songs.entries)

    print(lyrics[15])


def __clean() -> None:
    pass


def __analyze() -> None:
    pass


def __compare() -> None:
    pass


def __export() -> None:
    pass


def __persist() -> None:
    cache.dump_cache(cache_path)


if __name__ == "__main__":
    __setup()
    __interpret()
    __gather(years=[2007], songs=[SongContainer(artist="Rise Against", title="Satellite")])
    __clean()
    __analyze()
    __compare()
    __export()
