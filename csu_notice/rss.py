from fastapi import FastAPI, Response
from nonebot import get_asgi

from .config import _config
from .data_source import get_notices

app: FastAPI = get_asgi()


@app.get("/csu/{tag}")
async def _(tag: str) -> Response:
    if _config.enable_rss:
        rss = """<?xml version="1.0" encoding="UTF-8"?>
<rss  xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
    <channel>
        <title><![CDATA[中南大学校内通知]]></title>
        <link>http://tz.its.csu.edu.cn/Home/Release_TZTG/0-</link>
        <atom:link href="http://tz.its.csu.edu.cn/Home/Release_TZTG/0" rel="self" type="application/rss+xml" />
        <description><![CDATA[中南大学校内通知]]></description>
        <generator>CSU-Notice</generator>
        <webMaster>j1g5aw@foxmail.com (Jigsaw)</webMaster>
        <language>zh-cn</language>
"""
        notices = await get_notices(
            _config.api_server, tag, _config.tag[tag] - 10, False
        )
        notices.reverse()
        for notice in notices:
            rss += f"""        <item>
        <title><![CDATA[{notice["title"]}]]></title>
        <description><![CDATA[{notice["title"]}]]></description>
        <guid isPermaLink="false">{notice["uri"]}</guid>
        <link>{notice["uri"]}</link>
        <author><![CDATA[{notice["from"]}]]></author>
    </item>"""

        rss += """    </channel>
</rss>"""
        return Response(
            content=rss,
            media_type="application/xml",
        )
    else:
        return Response(status_code=404)
