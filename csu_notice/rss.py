from fastapi import FastAPI, Response
from nonebot import get_asgi
from sqlmodel import col, select
from sqlmodel.ext.asyncio.session import AsyncSession

from .config import _config
from .data import Notice, engine
from .filter import filter_notice, filter_out_notice

app: FastAPI = get_asgi()


@app.get("/csu")
async def _(
    filter: str = "",
    filter_author: str = "",
    filterout: str = "",
    filterout_author: str = "",
) -> Response:
    print(_config.enable_rss)
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
        async with AsyncSession(engine) as session:
            statement = select(Notice).order_by(col(Notice.id).desc()).limit(10)
            notices = await session.execute(statement)
        for notice in notices:
            notice = notice[0]
            if filter_notice(
                notice,
                [_ for _ in filter_author.split("|") if _],
                [_ for _ in filter.split("|") if _],
            ) and filter_out_notice(
                notice,
                [_ for _ in filterout_author.split("|") if _],
                [_ for _ in filterout.split("|") if _],
            ):
                rss += f"""        <item>
            <title><![CDATA[{notice.title}]]></title>
            <description><![CDATA[{notice.content}]]></description>
            <guid isPermaLink="false">{notice.url}</guid>
            <link>{notice.url}</link>
            <author><![CDATA[{notice.author}]]></author>
        </item>"""
        rss += """    </channel>
    </rss>"""
        return Response(
            content=rss,
            media_type="application/xml",
        )
    else:
        return Response(status_code=404)
