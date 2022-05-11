from api.lyrics import AZLyricRunner, SongContainer


# Lifecycle Functions

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
