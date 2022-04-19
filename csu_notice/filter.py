from typing import List

from .data import Notice


def filter_notice(notice: Notice, from_: List[str], keyword: List[str]) -> bool:
    _ = True if not keyword else False
    for key_word in keyword:
        if key_word in notice.title:
            _ = True
            break
    return _ and (True if not from_ else notice.author in from_)


def filter_out_notice(notice: Notice, from_: List[str], keyword: List[str]) -> bool:
    _ = True
    for key_word in keyword:
        if key_word in notice.title:
            _ = False
            break
    return _ and (True if not from_ else notice.author not in from_)


def format_notice(notice: Notice) -> str:
    return "｜".join([notice.title, notice.author]) + "\n" + notice.url
