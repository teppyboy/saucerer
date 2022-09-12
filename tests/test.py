from saucerer import Saucerer

saucerer = Saucerer()
results = saucerer.search(image_url="https://ayayaxyz.tretrauit.repl.co/pixiv/https:/i.pximg.net/img-original/img/2022/09/04/04/53/47/100980966_p0.jpg")
for result in results:
    print("Hidden: {}, Match: {}, Source: {}, Title: {}, Author: {}".format(result.hidden, result.match_percentage, result.sauce.url, result.sauce.name, result.sauce.user.name))