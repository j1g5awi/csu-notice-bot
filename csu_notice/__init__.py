from nonebot import get_bots
from nonebot.plugin import on_shell_command, require
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import GroupMessageEvent, Bot
from nonebot.adapters.cqhttp.permission import GROUP_ADMIN, GROUP_OWNER

from .parser import _parser
from .config import _config
from .handle import Handle
from .data_source import get_latest_head, get_latest_notice, get_notices

scheduler = require("nonebot_plugin_apscheduler").scheduler

csu_notice = on_shell_command(
    "csu_notice",
    parser=_parser,
    permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN,
    priority=5,
)


@scheduler.scheduled_job("cron", minute="*", id="csu_notice")
async def _():
    for tag_name in _config.tags:
        tag = _config.tags.get(tag_name)
        if tag.latest_head:
            notices = await get_notices(tag=tag_name, head=tag.latest_head)
        _config.tags.get(tag_name).latest_head = await get_latest_head(tag=tag_name)
        _config.dump()
        for notice in notices:
            for group_id in tag.enabled_group:
                for bot in get_bots().values():
                    if isinstance(bot, Bot):
                        await bot.send_group_msg(
                            group_id=group_id,
                            message=notice,
                        )


@csu_notice.handle()
async def _(bot: Bot, event: GroupMessageEvent, state):
    args = state["args"]
    args.group_id = event.group_id
    if hasattr(args, "handle") and args.handle:
        print(args.handle)
        message = await getattr(Handle, args.handle)(args)
        if message:
            await bot.send(event, message)
    else:
        await bot.send(event, await get_latest_notice("main"))
