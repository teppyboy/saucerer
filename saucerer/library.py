import aiohttp
import io
from aiohttp.client_exceptions import ClientError
from urllib.parse import urlparse
from os import PathLike
from pathlib import Path
from .constants import *
from .classes import SearchResult
from .exceptions import *
from bs4 import BeautifulSoup, element


def _validate_url(url: str) -> bool:
    result = urlparse(url=url)
    return all([result.scheme, result.netloc])


class Saucerer:
    def __init__(self):
        self._session: aiohttp.ClientSession = None

    async def __aenter__(self):
        await self.init()
        return self

    async def __aexit__(self, exc_t, exc_v, exc_tb):
        await self.close()

    async def init(self):
        if self._session:
            return
        self._session = aiohttp.ClientSession()
        self._session.headers.update(HEADERS)

    async def close(self):
        if not self._session:
            return
        await self._session.close()

    def _parse(self, search: str, hidden: bool = True) -> list[SearchResult]:
        html = BeautifulSoup(search, "html.parser")
        results = []
        for result in html.find(id="mainarea").find(id="middle").children:
            if result is None:
                continue
            if not isinstance(result, element.Tag):
                continue
            if (
                result.get("id") == "result-hidden-notification"
                or result.get("id") == "smalllogo"
            ):
                continue
            image_sauce = SearchResult.from_html(result)
            if not image_sauce or (image_sauce.hidden and not hidden):
                continue
            results.append(image_sauce)
        return results

    async def search(
        self,
        image: PathLike | str | io.BufferedIOBase | io.TextIOBase | io.BytesIO,
        databases: list[int] = None,
        hidden: bool = True,
    ) -> list[SearchResult]:
        params = {}
        await self.init()
        if isinstance(image, io.BufferedIOBase):
            params.update({"file": image.read()})
        elif isinstance(image, io.TextIOBase):
            params.update({"url": image.read(), "file": None})
        elif _validate_url(image):
            params.update({"url": image, "file": None})
        else:
            file = Path(image)
            params.update({"file": file.read_bytes()})

        if databases:
            for db in databases:
                params.update({"dbs[]", (None, db)})
        try:
            rsp = await self._session.post(
                "https://saucenao.com/search.php",
                data=params,
            )
        except ClientError as e:
            raise UploadError(e)
        try:
            return self._parse(await rsp.text(), hidden=hidden)
        except Exception as e:
            raise ParseError(e)
