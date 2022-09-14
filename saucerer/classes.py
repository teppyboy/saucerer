from bs4 import BeautifulSoup, element


class SauceUser:
    def __init__(self, name: str, url: str):
        self._name = name
        self._url = url

    @property
    def name(self) -> str:
        return self._name

    @property
    def url(self) -> str:
        return self._url


class Sauce:
    def __init__(
        self, name: str, url: str, sauce_id: int, user_name: str, user_url: str
    ):
        self._name = name
        self._url = url
        self._id = sauce_id
        self._user = SauceUser(user_name, user_url)

    @property
    def name(self) -> str:
        return self._name

    @property
    def url(self) -> str:
        return self._url

    @property
    def id(self) -> int:
        return self._id

    @property
    def user(self) -> SauceUser:
        return self._user


class SearchResult:
    def __init__(
        self,
        hidden: bool,
        image_url: str,
        image_title: str,
        match_percentage: float,
        sauce_url: str,
        sauce_id: int,
        user_url: str,
        user_name: str,
    ):
        self._image_url = image_url
        self._hidden = hidden
        self._match_percentage = match_percentage
        self._sauce = Sauce(image_title, sauce_url, sauce_id, user_name, user_url)

    @property
    def hidden(self) -> bool:
        return self._hidden

    @property
    def image_url(self) -> str:
        return self._image_url

    @property
    def match_percentage(self) -> float:
        return self._match_percentage

    @property
    def sauce(self) -> Sauce:
        return self._sauce

    @staticmethod
    def from_html(html: BeautifulSoup) -> "SearchResult":
        # Sauce variables
        source_url = None
        source_id = None
        user_url = None
        user_name = None
        hidden = False
        if html.get("class") and "hidden" in html.get("class"):
            hidden = True
        html = html.find("tr", recursive=True)
        if not html:
            return
        sauce_info = html.find(class_="resultcontent", recursive=True)
        sauce_info_column = sauce_info.find(class_="resultcontentcolumn")

        for info in sauce_info_column.find_all(class_="linkify"):
            prev_element = info.previous_element
            if not isinstance(prev_element, element.NavigableString):
                continue
            if "ID" in prev_element:
                source_url = info.get("href")
                source_id = int(info.decode_contents())
            elif any(s in prev_element for s in ["Member", "Creator", "Author"]):
                user_url = info.get("href")
                user_name = info.decode_contents()
        image = html.find(class_="resultimage", recursive=True).find(
            "img", recursive=True
        )
        image_url = image.get("src")
        if image_url == "images/static/blocked.gif":
            image_url = image.get("data-src")
        image_title = (
            sauce_info.find(class_="resulttitle").find("strong").decode_contents()
        )
        match_percentage = (
            float(
                html.find(
                    class_="resultsimilarityinfo", recursive=True
                ).decode_contents()[:-1]
            )
            / 100
        )
        return SearchResult(
            image_url=image_url,
            hidden=hidden,
            image_title=image_title,
            match_percentage=match_percentage,
            sauce_url=source_url,
            sauce_id=source_id,
            user_url=user_url,
            user_name=user_name,
        )
