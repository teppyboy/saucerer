from cgitb import html
from os import PathLike
from pathlib import Path
import requests
from saucerer.constants import *
from saucerer.classes import SearchResult
from bs4 import BeautifulSoup, element


class Saucerer:
    def __init__(self):
        self._session = requests.Session()
        self._session.headers.update(HEADERS)

    def _search_parse(self, search: str):
        html = BeautifulSoup(search, "html.parser")
        results = []
        for result in html.find(id="mainarea").find(id="middle").children:
            if not isinstance(result, element.Tag):
                continue
            if result is None:
                continue
            if (
                result.get("id") == "result-hidden-notification"
                or result.get("id") == "smalllogo"
            ):
                continue
            image_sauce = SearchResult.from_html(result)
            if not image_sauce:
                continue
            results.append(image_sauce)
        return results

    def search(
        self,
        file: PathLike | str = None,
        image_url: str = None,
        databases: list[int] = None,
    ) -> list[SearchResult]:
        if not file and not image_url:
            raise ValueError("At least a file or an url is required")
        file_name = None
        file_bytes = None
        if file:
            file = Path(file)
            file_name = file.name
            file_bytes = file.read_bytes()
        files_params = {"file": (file_name, file_bytes)}
        if image_url:
            files_params.update({"url": (None, image_url)})
        if databases:
            for db in databases:
                files_params.update({"dbs[]", (None, db)})
        rsp = self._session.post(
            "https://saucenao.com/search.php",
            files=files_params,
        )
        return self._search_parse(rsp.text)
