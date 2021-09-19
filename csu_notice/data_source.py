from typing import Any, List, Dict
from httpx import AsyncClient
from .config import _config


def format_notices(notices: List[Dict[str, Any]]) -> List[str]:
    message = []
    if notices:
        for notice in notices:
            message.append(
                notice.get("title")
                + " | "
                + notice.get("from")
                + "\n"
                + notice.get("uri")
                + "\n"
                + "这里本来应该有一张图"
            )
    return message


async def get_lateset_head(tag: str) -> int:
    async with AsyncClient(base_url=f"{_config.api_server}/{tag}") as client:
        res = await client.get("head")
    return int(res.json().get("msg"))


async def get_notices(tag: str, head: int) -> List[str]:
    async with AsyncClient(base_url=f"{_config.api_server}/{tag}") as client:
        res = await client.post("", params={"head": head})
    return format_notices(res.json().get("notices"))
