from typing import Dict, List, Any


def filter_notice(notice: Dict[str, Any], from_: List[str], keyword: List[str]) -> int:
    _ = 1 if notice["from"] in from_ else 0
    for key_word in keyword:
        if key_word in notice["message"]:
            _ = _ + 1
            break
    return _


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
