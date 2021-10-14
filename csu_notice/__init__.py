from nonebot import get_bots
from nonebot.plugin import on_shell_command, require
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import GroupMessageEvent, Bot
from nonebot.adapters.cqhttp.permission import GROUP_ADMIN, GROUP_OWNER

from .parser import _parser
from .config import _config
from .handle import Handle
from .utils import filter_notice, filter_out_notice, format_notice
from .data_source import get_notices, get_latest_head

scheduler = require("nonebot_plugin_apscheduler").scheduler

csu_notice = on_shell_command(
    "csu_notice",
    parser=_parser,
    permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN,
    priority=5,
)


@scheduler.scheduled_job("cron", minute="*/5", id="csu_notice")
async def _():
    if not _config.api_server:
        return
    notices = []
    for tag, latest_head in _config.tag.items():
        for notice in await get_notices(_config.api_server, tag, latest_head):
            notice["tag"] = tag
            notice["message"] = format_notice(notice,_config.enable_content)
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


@csu_notice.handle()
async def _(bot: Bot, event: GroupMessageEvent, state):
    args = state["args"]
    args.group_id = str(event.group_id)
    if hasattr(args, "handle") and args.handle:
        message = await getattr(Handle, args.handle)(args)
        if message:
            await bot.send(event, message)
