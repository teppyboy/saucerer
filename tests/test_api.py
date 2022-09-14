from saucerer import Saucerer

saucerer = Saucerer()


def test_search_file():
    results = saucerer.search(file="./images/100980966_p0.jpg")
    assert len(results) > 0
    assert results[0].sauce.id == 100980966


def test_search_url():
    results = saucerer.search(
        image_url="https://ayayaxyz.tretrauit.repl.co/pixiv/https:/i.pximg.net/img-original/img/2022/09/04/04/53/47/100980966_p0.jpg"
    )
    assert len(results) > 0
    assert results[0].sauce.id == 100980966
