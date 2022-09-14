# Saucerer

A SauceNAO web scrapper written in Python.

## Usage

```python
saucerer = Saucerer()
# search for sauce from an image file
search_result = saucerer.search(file="./images/100980966_p0.jpg")
# or from an url
search_result = saucerer.search(file="https://ayayaxyz.tretrauit.repl.co/pixiv/https:/i.pximg.net/img-original/img/2022/09/04/04/53/47/100980966_p0.jpg")
# print the first sauce url
print(search_result[0].sauce.url)
```
