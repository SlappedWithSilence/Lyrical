from api.lyrics import AZLyricRunner, SongContainer


# Lifecycle Functions
from src.api.billboard import BillboardRunner


def __gather() -> None:
    pass


def __clean() -> None:
    pass


def __analyze() -> None:
    pass


def __compare() -> None:
    pass


def __export() -> None:
    pass


if __name__ == "__main__":
    test_song = SongContainer("Three Days Grace", "Riot")
    runner = AZLyricRunner()

    result = runner.get(test_song)

    print(result.lyrics)

    runner = BillboardRunner()
    print(runner.get(year=2006).entries)
