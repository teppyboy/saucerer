# Saucerer

A SauceNAO web scrapper written in Python.

## Usage

```python
from saucerer import Saucerer
import asyncio
# Either using async with
async with Saucerer() as saucerer:
    # search for sauce from an image file
    search_result = saucerer.search(file="./images/100980966_p0.jpg")
    # print the first sauce url
    print(search_result[0].sauce.url)
# or initialize & close it manually
async def main():
    saucerer = Saucerer()
    # search for sauce from an url
    search_result = await saucerer.search("https://ayayaxyz.tretrauit.repl.co/pixiv/raw?url=https:/i.pximg.net/img-original/img/2022/09/04/04/53/47/100980966_p0.jpg")
    await saucerer.close()
    # print the first sauce url
    print(search_result[0].sauce.url)
asyncio.run(main())
```

## Documentation

https://tretrauit.gitlab.io/saucerer-docs

## License

[MIT license](LICENSE)
