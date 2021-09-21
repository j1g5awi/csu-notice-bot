from argparse import Namespace

from .config import _config
from .data_source import get_latest_notice


class Handle:
    @classmethod
    async def sub(cls, args: Namespace) -> str:
        if not args.tag:
            args.tag = ["main"]
        for tag_name in args.tag:
            tag = _config.tags.get(tag_name)
            if tag and args.group_id not in tag.enabled_group:
                tag.enabled_group.append(args.group_id)
        _config.dump()

    @classmethod
    async def unsub(cls, args: Namespace) -> str:
        if not args.tag:
            args.tag = _config.tags.keys()
        for tag_name in args.tag:
            tag = _config.tags.get(tag_name)
            if tag and args.group_id in tag.enabled_group:
                tag.enabled_group.remove(args.group_id)
        _config.dump()

    @classmethod
    async def set(cls, args: Namespace) -> str:
        old_api_server = _config.api_server
        try:
            _config.api_server = args.api_server
            await get_latest_notice("main")
            message = "成功设置通知 API 服务器！"
            _config.dump()
        except:
            _config.api_server = old_api_server
            message = "服务器未通过检测，设置失败！"
        return message
