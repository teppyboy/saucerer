from saucerer import Saucerer
import asyncio

loop = asyncio.new_event_loop()
saucerer = Saucerer()

for result in loop.run_until_complete(saucerer.search("https://ayayaxyz.tretrauit.repl.co/pixiv/raw?url=https://i.pximg.net/img-original/img/2022/01/05/00/00/16/95304656_p0.png")):
    print(result.as_dict())
loop.run_until_complete(saucerer.close())
