from typing import List, Dict, Any
from httpx import AsyncClient
from .config import _config


def format_notice(notice: Dict[str, Any]) -> str:
    return (
        notice.get("title")
        + " | "
        + notice.get("from")
        + "\n"
        + notice.get("uri")
        + "\n"
        + "这里本来应该有一张图"
    )


async def get_latest_head(tag: str) -> int:
    async with AsyncClient(base_url=f"{_config.api_server}/{tag}") as client:
        res = await client.get("head")
    return int(res.json().get("msg"))


async def get_notices(tag: str, head: int) -> List[str]:
    async with AsyncClient(base_url=f"{_config.api_server}/{tag}") as client:
        res = await client.post("", params={"head": head})
    notices = res.json().get("notices")
    if head and notices:
        return [format_notice(notice) for notice in notices]
    else:
        return []


async def get_latest_notice(tag: str) -> str:
    async with AsyncClient(base_url=f"{_config.api_server}/{tag}") as client:
        res = await client.get("latest")
    return format_notice(res.json().get("notice"))
