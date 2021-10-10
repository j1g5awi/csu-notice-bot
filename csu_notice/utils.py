from typing import Dict, List, Any, Optional


def filter_notice(notice: Dict[str, Any], from_: List[str], keyword: List[str]) -> bool:
    _ = True if not keyword else False
    for key_word in keyword:
        if key_word in notice["message"]:
            _ = True
            break
    return _ and (True if not from_ or notice["from"] in from_ else False)


def filter_out_notice(
    notice: Dict[str, Any], from_: List[str], keyword: List[str]
) -> bool:
    _ = True
    for key_word in keyword:
        if key_word in notice["message"]:
            _ = False
            break
    return _ and (True if not (from_ and notice["from"] in from_) else False)


def format_notice(notice: Dict[str, Any]) -> str:
    return (
        notice["title"]
        + " | "
        + notice["from"]
        + "\n"
        + notice["uri"]
        + "\n"
        + (notice["content"] if notice["content"] else "这里本来应该有一张图")
    )
