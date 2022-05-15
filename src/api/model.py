import re


class SongContainer:

    def __init__(self, artist: str, title: str) -> None:
        self.lyrics: str = None
        self.failed: bool = False

        self.proper = {"artist": artist, "title": title}

        self.title = re.sub('[^A-Za-z0-9]+', "", title.lower())  # Remove all non-alpha-numeric chars
        self.artist = re.sub('[^A-Za-z0-9]+', "", artist.lower())  # Remove all non-alpha-numeric chars
        if self.artist.startswith("the"):  # Remove "the" from the front of the artist string
            self.artist = self.artist[3:]
        self.artist = self.artist.split("featuring")[0]

    def set_lyrics(self, lyrics: str) -> any:
        self.lyrics = lyrics
        return self

    def set_failed(self, status: bool) -> any:
        self.failed = status
        return self

    def __str__(self) -> str:
        return f"{self.artist} - {self.title}"