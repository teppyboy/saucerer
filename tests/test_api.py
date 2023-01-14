from saucerer import Saucerer
import pytest


@pytest.mark.asyncio
async def test_search_file():
    async with Saucerer() as saucerer:
        results = await saucerer.search("./tests/images/100980966_p0.jpg")
    assert len(results) > 0
    assert results[0].sauce.id == 100980966


@pytest.mark.asyncio
async def test_search_url():
    async with Saucerer() as saucerer:
        results = await saucerer.search(
            "https://ayayaxyz.tretrauit.repl.co/pixiv/raw?url=https:/i.pximg.net/img-original/img/2022/09/04/04/53/47/100980966_p0.jpg"
        )
    assert len(results) > 0
    assert results[0].sauce.id == 100980966
