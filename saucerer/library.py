from cgitb import html
from os import PathLike
from pathlib import Path
import requests
from saucerer.constants import *
from bs4 import BeautifulSoup, element


class SearchResult:
    def __init__(
        self,
        image_url: str,
        image_title: str,
        match_percentage: float,
        source_url: str,
        source_id: int,
        user_url: str
    ):
        self._image_url = image_url
        self._image_title = image_title
        self._match_percentage = match_percentage
        self._source_url = source_url
        self._source_id = source_id
        self._user_url = user_url

    @property
    def image_url(self):
        return self._image_url

    @staticmethod
    def from_html(html: BeautifulSoup):
        html = html.find("tr", recursive=True)
        sauce_info = html.find(class_="resultcontent", recursive=True)
        sauce_info_column = sauce_info.find(class_="resultcontentcolumn")

        for info in sauce_info_column.find_all(class_="linkify"):
            prev_element = info.previous_element
            print(prev_element)
            if not isinstance(prev_element, element.NavigableString):
                continue
            if "ID" in prev_element:
                source_url = info["href"]
                source_id = int(info.decode_contents())
            elif any(s in prev_element for s in ["Member", "Creator", "Author"]):
                user_url = info["href"]
        image = html.find(class_="resultimage", recursive=True).find("img", recursive=True)
        print(image)
        image_url = image["src"]
        image_title = (
            sauce_info.find(class_="resulttitle").find("strong").decode_contents()
        )
        match_percentage = float(
            html.find(class_="resultsimilarityinfo", recursive=True).decode_contents()[
                :-1
            ]
        )
        return SearchResult(
            image_url=image_url,
            image_title=image_title,
            match_percentage=match_percentage,
            source_url=source_url,
            source_id=source_id,
            user_url=user_url
        )


class Saucerer:
    def __init__(self):
        self._session = requests.Session()
        self._session.headers.update(HEADERS)

    def _search_parser(self, search: str):
        html = BeautifulSoup(search, "html.parser")
        results = []
        for result in html.find(id="mainarea").find(id="middle").children:
            # print(result)
            if not isinstance(result, element.Tag):
                continue
            if (
                result.get("id") == "result-hidden-notification"
                or result.get("id") == "smalllogo"
            ):
                continue
            results.append(SearchResult.from_html(result))
        return results

    def search(
        self,
        file: PathLike | str = None,
        image_url: str = None,
        databases: list[int] = None,
    ):
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
        return self._search_parser(rsp.text)


def main():
    saucerer = Saucerer()
    results = saucerer.search(image_url="https://ayayaxyz.tretrauit.repl.co/pixiv/https:/i.pximg.net/img-original/img/2022/09/04/04/53/47/100980966_p0.jpg")
    print(results)
