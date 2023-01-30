class Author:
    """An author information

    Attributes:
        name: A string containing the author name
        url: A string containing the author url in the sauce website
    """

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
        """Convert the current class to a dict"""
        return {
            "name": self._name,
            "url": self._url,
        }


class Illustration:
    """An illustration information

    Attributes:
        name: A string containing the illust name
        url: A string containing the url to the illust
        id: A string or an integer containing the illust id in the sauce website
        author: An `Author` class containing the author information
        artist: Alias for `author`
    """

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

    @property
    def artist(self) -> Author:
        return self._author

    def as_dict(self) -> dict:
        """Convert the current class to a dict"""
        return {
            "name": self._name,
            "url": self._url,
            "id": self._id,
            "author": self._author.as_dict(),
        }


class MiscInfo:
    """A miscellaneous information (usually alternative url to the image)

    Attributes:
        provider: A string containing the image provider
        url: A string containing the url to the image
    """

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
        """Convert the current class to a dict"""
        return {"provider": self._provider, "url": self._url}


class Sauce:
    """A sauce

    Attributes:
        TODO
    """

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
        self._illust = Illustration(
            image_title, sauce_url, sauce_id, user_name, user_url
        )
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
        """Convert the current class to a dict"""
        return {
            "hidden": self._hidden,
            "image_url": self._image_url,
            "match_percentage": self._match_percentage,
            "material": self._material,
            "characters": self._characters,
            "misc_info": [x.as_dict() for x in self._misc_info],
            "illust": self._illust.as_dict(),
        }


class RetryLink:
    """A retry link

    Attributes:
        title: A string containing the search provider
        url: A string containing the url to the image search result
    """

    def __init__(self, title: str, url: str):
        self._title = title
        self._url = url

    @property
    def title(self) -> str:
        return self._title

    @property
    def url(self) -> str:
        return self._url

    def as_dict(self) -> dict:
        """Convert the current class to a dict"""
        return {"title": self._title, "url": self._url}


class SearchResult:
    def __init__(
        self, sauces: list[Sauce], retry_links: list[RetryLink], my_image_url: str
    ):
        self._sauces = sauces
        self._retry_links = retry_links
        self._my_image_url = my_image_url

    @property
    def sauces(self) -> list[Sauce]:
        return self._sauces

    @property
    def retry_links(self) -> list[RetryLink]:
        return self._retry_links

    @property
    def my_image_url(self) -> str:
        return self._my_image_url

    def as_dict(self) -> dict:
        """Convert the current class to a dict"""
        return {
            "sauces": [x.as_dict() for x in self._sauces],
            "retry_links": [x.as_dict() for x in self._retry_links],
            "my_image_url": self._my_image_url,
        }
