import aiohttp
import io
from aiohttp.client_exceptions import ClientError
from logging import Logger
from urllib.parse import urlparse
from os import PathLike, getenv
from pathlib import Path
from .constants import *
from .classes import MiscInfo, Sauce, SearchResult
from .exceptions import *
from bs4 import BeautifulSoup, element


def _validate_url(url: str) -> bool:
    result = urlparse(url=url)
    return all([result.scheme, result.netloc])


class Saucerer:
    def __init__(self):
        self._session: aiohttp.ClientSession = None
        self._logger = Logger("saucerer", getenv("SAUCERER_LOG_LEVEL", "INFO"))

    async def __aenter__(self):
        await self.init()
        return self

    async def __aexit__(self, exc_t, exc_v, exc_tb):
        await self.close()

    async def init(self) -> None:
        if self._session:
            return
        self._session = aiohttp.ClientSession()
        self._session.headers.update(HEADERS)

    async def close(self) -> None:
        if not self._session:
            return
        await self._session.close()

    def _prev_element(self, obj):
        prevs = obj.previous_elements
        for prev in prevs:
            if self._decode(prev).strip() not in ["", None]:
                return prev

    def _get(self, obj, text: str) -> str:
        if isinstance(obj, element.NavigableString):
            return obj.get_text()
        return obj.get(text)

    def _decode(self, obj) -> str:
        if isinstance(obj, element.NavigableString):
            return obj.get_text()
        return obj.decode_contents()

    def _parse_sauce(self, html: BeautifulSoup) -> Sauce:
        # Sauce variables
        source_url = None
        source_id = None
        user_url = None
        user_name = None
        image_title = None
        material = None
        characters = None

        hidden = False
        html = html.find("tr", recursive=True)
        if not html:
            return
        if html.get("class") and "hidden" in html.get("class"):
            hidden = True
        sauce_info = html.find(class_="resultcontent", recursive=True)
        for sauce_info_column in sauce_info.find_all(class_="resultcontentcolumn"):
            for info in sauce_info_column.children:
                prev = self._prev_element(info)
                if "ID" in prev:
                    source_url = self._get(info, "href")
                    source_id = int(self._decode(info))
                elif "Source" in prev:
                    source_url = self._get(info, "href")
                    source_str = self._decode(info)
                    if "#" in source_str:
                        source_id = int(source_str.split("#")[1].strip())
                    elif "/" in source_str:
                        source_id = source_str.split("/")[:-1].strip()
                elif any(x in prev for x in ["Member", "Creator", "Author"]):
                    user_url = self._get(info, "href")
                    user_name = self._decode(info)
                elif any(x in prev for x in ["Material"]):
                    material = self._decode(info)
                elif "Characters" in prev:
                    characters = self._decode(info)
        image = html.find(class_="resultimage", recursive=True).find(
            "img", recursive=True
        )
        image_url = image.get("src")
        if image_url == "images/static/blocked.gif":
            image_url = image.get("data-src")
        for element in sauce_info.find(class_="resulttitle").children:
            prev = self._prev_element(element)
            if any(x in self._decode(prev) for x in ["Member", "Creator", "Author"]):
                user_name = self._decode(element)
            elif self._decode(prev) != user_name:
                image_title = self._decode(prev)
        match_info = html.find(class_="resultmatchinfo")
        match_percentage = (
            float(
                self._decode(match_info.find(
                    class_="resultsimilarityinfo"
                ))[:-1]
            )
            / 100
        )
        misc_info = []
        for element in match_info.find(class_="resultmiscinfo").children:
            prev = self._prev_element(element)
            if not element.get("href"):
                continue
            url = element.get("href")
            provider = element.contents[0].get("src").split("/")[-1][:-4]
            misc_info.append(MiscInfo(provider=provider, url=url))
            
        return Sauce(
            image_url=image_url,
            hidden=hidden,
            image_title=image_title,
            match_percentage=match_percentage,
            sauce_url=source_url,
            sauce_id=source_id,
            user_url=user_url,
            user_name=user_name,
            material=material,
            characters=characters,
            misc_info=misc_info,
        )

    def _parse(self, search: str, hidden: bool = True) -> SearchResult:
        html = BeautifulSoup(search, "html.parser")
        sauces = []
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
            image_sauce = self._parse_body(result)
            if not image_sauce or (image_sauce.hidden and not hidden):
                continue
            sauces.append(image_sauce)
        return SearchResult(sauces=sauces)

    async def search(
        self,
        image: PathLike | str | io.BufferedIOBase | io.TextIOBase | io.BytesIO,
        databases: list[int] = None,
        hidden: bool = True,
    ) -> SearchResult:
        params = {}
        await self.init()
        if isinstance(image, io.BufferedIOBase):
            params.update({"file": image.read()})
        elif isinstance(image, io.TextIOBase):
            params.update({"url": image.read(), "file": None})
        elif _validate_url(image):
            params.update({"url": image, "file": None})
        elif isinstance(image, PathLike):
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
