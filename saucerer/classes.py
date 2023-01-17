class Author:
    def __init__(self, name: str, url: str):
        self._name = name
        self._url = url

    @property
    def name(self) -> str:
        return self._name

    @property
    def url(self) -> str:
        return self._url

    def as_dict(self) -> dict:
        return {
            "name": self._name,
            "url": self._url,
        }


class Illustration:
    def __init__(
        self, name: str, url: str, sauce_id: int | str, user_name: str, user_url: str
    ):
        self._name = name
        self._url = url
        self._id = sauce_id
        self._author = Author(user_name, user_url)

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
    def author(self) -> Author:
        return self._author

    def as_dict(self) -> dict:
        return {
            "name": self._name,
            "url": self._url,
            "id": self._id,
            "author": self._author.as_dict()
        }

class MiscInfo:
    def __init__(self, provider: str, url: str) -> None:
        self._provider = provider
        self._url = url

    @property
    def provider(self) -> bool:
        return self._provider

    @property
    def url(self) -> str:
        return self._url

    def as_dict(self) -> dict:
        return {
            "provider": self._provider,
            "url": self._url
        }

class Sauce:
    def __init__(
        self,
        hidden: bool,
        image_url: str,
        image_title: str,
        match_percentage: float,
        sauce_url: str,
        sauce_id: int | str,
        user_url: str,
        user_name: str,
        material: str,
        characters: str,
        misc_info: list[MiscInfo],
    ) -> None:
        self._image_url = image_url
        self._hidden = hidden
        self._match_percentage = match_percentage
        self._material = material
        self._characters = characters
        self._illust = Illustration(image_title, sauce_url, sauce_id, user_name, user_url)
        self._misc_info = misc_info

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
    def illust(self) -> Illustration:
        return self._illust

    @property
    def material(self) -> str:
        return self._material

    @property
    def characters(self) -> str:
        return self._characters

    @property
    def misc_info(self) -> list[MiscInfo]:
        return self._misc_info

    def as_dict(self) -> dict:
        return {
            "hidden": self._hidden,
            "image_url": self._image_url,
            "match_percentage": self._match_percentage,
            "material": self._material,
            "characters": self._characters,
            "misc_info": [x.as_dict() for x in self._misc_info],
            "illust": self._illust.as_dict()
        }

class SearchResult:
    def __init__(self, sauces: list[Sauce]):
        self._sauces = sauces

    @property
    def sauces(self) -> list[Sauce]:
        return self._sauces

    def as_dict(self) -> dict:
        return {
            "sauces": [x.as_dict() for x in self._sauces]
        }