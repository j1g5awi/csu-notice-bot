from base64 import b64encode

import httpx
from pyquery import PyQuery

from .config import _config
from .data import Notice

cookies = httpx.get("http://tz.its.csu.edu.cn").cookies


async def login():
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "http://tz.its.csu.edu.cn/Home/PostLogin",
            data={
                "user": _config.username,
                "pwd": b64encode(_config.password.encode("utf-8")).decode(),
            },
            cookies=cookies,
        )
        if resp.status_code == 200 and resp.text == "1":
            return True
        else:
            return False


async def fetch_notices():
    async with httpx.AsyncClient() as client:
        try_count = 0
        while try_count < 3:
            try:
                notices = []
                resp = await client.get("http://tz.its.csu.edu.cn", cookies=cookies)
                pq = PyQuery(resp.text)
                for notice in list(pq("tr").items())[5:25]:
                    notice = list(notice("td").items())
                    notices.append(
                        Notice(
                            title=notice[3].text(),
                            author=notice[4].text(),
                            updated=notice[6].text(),
                            url="http://tz.its.csu.edu.cn"
                            + notice[3]("a").attr("onclick")[14:68],
                        )
                    )
                return notices
            except httpx.ReadTimeout:
                try_count += 1
        return []


async def fetch_per_page(url: str):
    async with httpx.AsyncClient() as client:
        try_count = 0
        while try_count < 3:
            try:
                resp = await client.post(url, cookies=cookies)
                return resp.text
            except httpx.ReadTimeout:
                try_count += 1
