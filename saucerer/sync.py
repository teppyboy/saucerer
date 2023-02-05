import asyncio
import io
from os import PathLike
from .library import Saucerer


class SaucererSync:
    def __init__(self) -> None:
        self._loop = asyncio.new_event_loop()
        self._saucerer = Saucerer()

    def init(self):
        """Initialize Saucerer
        """
        self._loop.run_until_complete(self._saucerer.init())

    def close(self):
        self._loop.run_until_complete(self._saucerer.close())

    def search(
        self,
        image: PathLike | str | io.BufferedIOBase | io.TextIOBase | io.BytesIO,
        databases: list[int] = None,
        hidden: bool = True,
    ):
        """
        Search the image for the image sauces.

        Args:
            image: The image to search for sauces, can be a url, a path or any IO objects
            databases: The database ids to whitelist (default is `None`)
            hidden: Show image with low similarity (default is `True`)

        Returns:
            A `SearchResult` object containing the search result, which then can be converted
            to a dict by using `as_dict()`

        Raises:
            UploadError: Error occurred while uploading the image
            SauceNAOError: Server error
            ParseError: The module couldn't parse the result text
        """
        return self._loop.run_until_complete(
            self._saucerer.search(image=image, databases=databases, hidden=hidden)
        )
