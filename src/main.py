from multiprocessing.dummy import Pool as ThreadPool

from api.lyrics import get_lyrics, SongContainer
from api.billboard import BillboardRunner
from persistance.cache import get_cache


def __setup():
    """Perform system setup functions"""
    pass


def __interpret():
    """Generate a list of content to gather from user input"""
    pass


def __gather(years: list[int], songs: list[SongContainer]) -> None:
    """Gather requested content from third-party sources"""
    # Set up runners
    runner = BillboardRunner()

    # Get charts
    for year in years:
        if year not in get_cache()["charts"]["yearly"]:
            songs = runner.get(year=year)
            get_cache()["charts"]["yearly"][year] = songs

    # Get lyrics
    worker_pool = ThreadPool(1)

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


if __name__ == "__main__":
    __setup()
    __interpret()
    __gather(years=[2007], songs=[SongContainer(artist="Rise Against", title="Satellite")])
    __clean()
    __analyze()
    __compare()
    __export()
