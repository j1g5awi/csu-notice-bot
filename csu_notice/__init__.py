from .config import _config
from .data_source import get_lateset_head, get_notices
from nonebot import get_bots
from nonebot.plugin import on_command, require
from nonebot.adapters.cqhttp import GroupMessageEvent, Bot


scheduler = require("nonebot_plugin_apscheduler").scheduler

csu_notice = on_command("csu_notice", priority=5)


@scheduler.scheduled_job("cron", minute="*", id="csu_notice")
async def _():
    for tag_name in _config.tags:
        tag = _config.tags.get(tag_name)
        if tag.latest_head:
            notices = await get_notices(tag=tag_name, head=tag.latest_head)
        _config.tags.get(tag_name).latest_head = await get_lateset_head(tag=tag_name)
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
async def _(bot: Bot, event: GroupMessageEvent):
    message = ""
    if str(event.get_message()) == "on":
        if event.group_id not in config.enable_group:
            config.enable_group.append(event.group_id)
            message = "本群已添加到通知列表！"
        else:
            message = "本群已在通知列表中！"
    elif str(event.get_message()) == "off":
        if event.group_id in config.enable_group:
            config.enable_group.remove(event.group_id)
            message = "本群已从通知列表移除！"
        else:
            message = "本群不在通知列表中！"
    await bot.send(event, message)
