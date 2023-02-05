import argparse
from . import __version__
from .sync import SaucererSync
from .classes import RetryLink, Sauce
from .exceptions import SauceNAOError, SaucererError


def main():
    saucerer = SaucererSync()
    parser = argparse.ArgumentParser(
        prog="saucerer",
        description="A SauceNAO web scrapper written in Python",
        epilog="https://github.com/teppyboy/saucerer",
    )
    parser.add_argument("image",  help="The image to search for sauce, can be either an url or a path to the file.")
    parser.add_argument("-H", "--hidden", action="store_true", help='Show images "hidden" (low similarity) by SauceNAO.')
    parser.add_argument("--databases", type=int, nargs="*", help="Specify databases to search for sauce.")
    args = parser.parse_args()
    print(f"Saucerer v{__version__}: https://github.com/teppyboy/saucerer")
    print(f"Fetching sauce for {args.image}...")
    def _pp_sauces(sauces = list[Sauce]):
        s = "s" if len(sauces) > 1 else ''
        msg = f"Sauce{s}:\n"
        for i, v in enumerate(sauces):
            # Fix typing
            v: Sauce = v
            illust = v.illust
            author = illust.author
            misc_infos = v.misc_info
            msg += f"* Sauce {i}:\n"
            msg += f"  - Hidden: {v.hidden}\n"
            msg += f"  - Match: {v.match_percentage * 100}%\n"
            msg += f"  - Illust:\n"
            if illust.name:
                msg += f"    + Name: {illust.name}\n"
            msg += f"    + Url: {illust.url}\n"
            msg += f"    + ID: {illust.id}\n"
            if author.name and author.url:
                msg += f"    + Author:\n"
                if author.name:
                    msg += f"      - Name: {author.name}\n"
                if author.url:
                    msg += f"      - Url: {author.url}\n"
            if len(misc_infos) > 0:
                msg += f"    + Misc:\n"
                for misc_info in misc_infos:
                    msg += f"      - {misc_info.provider}: {misc_info.url}\n"
            msg += "\n"
        return msg
    def _pp_retry_links(retry_links: list[RetryLink]):
        s = "s" if len(retry_links) > 1 else ''
        msg = f"Retry link{s}:\n"
        for v in retry_links:
            msg += f"+ {v.title}: {v.url}\n"
        return msg

    def _main():
        try:
            result = saucerer.search(args.image, hidden=args.hidden)
        except SauceNAOError as e:
            print(f"Server returned error: {e}")
            return
        except SaucererError as e:
            print(f"Error occurred while parsing the result: {e}")
            return
        if len(result.sauces) == 0:
            print("No result was found...")
            _pp_retry_links(result.retry_links)
            return
        print(_pp_sauces(result.sauces))
    _main()
    saucerer.close()
