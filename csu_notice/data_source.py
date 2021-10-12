from typing import List, Dict, Any
from httpx import AsyncClient


async def get_latest_head(api_server: str, tag: str) -> int:
    async with AsyncClient(base_url=f"{api_server}/{tag}") as client:
        res = await client.get("head")
    return int(res.json().get("data"))


async def get_notices(api_server: str, tag: str, head: int) -> List[Dict[str, Any]]:
    async with AsyncClient(base_url=f"{api_server}/{tag}") as client:
        res = await client.post("", params={"head": head})
    notices = res.json().get("data")
    if head and notices:
        return notices
    else:
        return []


async def get_latest_notice(api_server: str, tag: str) -> Dict[str, Any]:
    async with AsyncClient(base_url=f"{api_server}/{tag}") as client:
        res = await client.get("latest")
    return res.json().get("data")
