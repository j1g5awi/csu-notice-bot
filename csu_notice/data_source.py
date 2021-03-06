from typing import Any, Dict, List

from httpx import AsyncClient


async def get_latest_head(api_server: str, tag: str) -> int:
    async with AsyncClient(base_url=f"{api_server}/{tag}") as client:
        res = await client.get("head")
    return int(res.json().get("data"))


async def get_notice(api_server: str, tag: str, id: int) -> Dict[str, Any]:
    async with AsyncClient(base_url=f"{api_server}/{tag}") as client:
        if id:
            res = await client.get(f"notice/{id}")
        else:
            res = await client.get("latest")
    notice = res.json().get("data")
    notice["content"] = await get_content(api_server, tag, notice["id"])
    return notice


async def get_content(api_server: str, tag: str, id: int) -> str:
    async with AsyncClient(base_url=f"{api_server}/{tag}") as client:
        res = await client.get(f"content/{id}")
    return res.json().get("data").get("content")


async def reload_content(api_server: str, tag: str, id: str, token: str) -> bool:
    async with AsyncClient(base_url=f"{api_server}/{tag}") as client:
        res = await client.get(f"reload/{token}/{id}")
    return res.json().get("msg") == "ok"


async def get_notices(
    api_server: str, tag: str, head: int, enable_content: bool
) -> List[Dict[str, Any]]:
    async with AsyncClient(base_url=f"{api_server}/{tag}") as client:
        res = await client.get(f"fetch/{head}")
    notices = res.json().get("data")
    if notices:
        if enable_content:
            for notice in notices:
                notice["content"] = await get_content(api_server, tag, notice["id"])
        return notices
    else:
        return []


async def search_notice(api_server: str, tag: str, title: str) -> List[Dict[str, Any]]:
    async with AsyncClient(base_url=f"{api_server}/{tag}") as client:
        res = await client.get(f"search/{title}")
    notices = res.json().get("data")
    if notices:
        return notices
    else:
        return []
