from argparse import Namespace

from nonebot import get_bots, get_driver
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.params import ShellCommandArgs
from nonebot.permission import SUPERUSER
from nonebot.plugin import on_shell_command, require
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel.sql.expression import select

from csu_notice.util import fetch_notices, fetch_per_page, login

from .config import _config
from .data import Notice, SQLModel, engine
from .handle import Handle
from .parser import _parser
from .rss import app

scheduler = require("nonebot_plugin_apscheduler").scheduler

csu_notice = on_shell_command(
    "csu_notice",
    parser=_parser,
    permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN,
    priority=5,
)

notices = set()


@get_driver().on_startup
async def _():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    async with AsyncSession(engine) as session:
        statement = select(Notice)
        results = await session.execute(statement)
        for notice in results:
            notices.add(notice[0].url)


@scheduler.scheduled_job("cron", minute="*", id="csu_notice")
async def _():
    await login()
    async with AsyncSession(engine) as session:
        for notice in await fetch_notices():
            if notice.url not in notices:
                notice.content = await fetch_per_page(notice.url)
                session.add(notice)
                notices.add(notice.url)
        await session.commit()

    """
    notices = []
    for tag, latest_head in _config.tag.items():
        for notice in await get_notices(
            _config.api_server, tag, latest_head, _config.enable_content
        ):
            notice["tag"] = tag
            notice["message"] = format_notice(notice)
            notices.append(notice)
        _config.tag[tag] = await get_latest_head(_config.api_server, tag)

    for group_id, group in _config.group.items():
        for index, notice in enumerate(notices):
            if not _config.limit or index < _config.limit:
                if (
                    notice["tag"] in group.subscribe
                    and filter_notice(notice, group.filter.from_, group.filter.keyword)
                    and filter_out_notice(
                        notice, group.filter_out.from_, group.filter_out.keyword
                    )
                ):
                    for bot in get_bots().values():
                        if isinstance(bot, Bot):
                            await bot.send_group_msg(
                                group_id=int(group_id),
                                message=notice["message"],
                            )
            else:
                break
    _config.dump()
"""


@csu_notice.handle()
async def _(bot: Bot, event: GroupMessageEvent, args: Namespace = ShellCommandArgs()):
    args.group_id = str(event.group_id)
    if hasattr(args, "handle") and args.handle:
        message = await getattr(Handle, args.handle)(args)
        if message:
            await bot.send(event, message)
    elif hasattr(args, "message"):
        await bot.send(event, args.message)
    else:
        await bot.send(event, _parser.format_help())
