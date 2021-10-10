from argparse import Namespace

from .config import _config, Group
from .data_source import get_latest_notice


class Handle:
    @classmethod
    async def sub(cls, args: Namespace):
        if not args.tag:
            args.tag = ["main"]
        for tag in args.tag:
            if tag in _config.tag:
                if args.group_id not in _config.group:
                    _config.group[args.group_id] = Group()
                if tag not in _config.group[args.group_id].subscribe:
                    _config.group[args.group_id].subscribe.append(tag)

        _config.dump()

    @classmethod
    async def unsub(cls, args: Namespace):
        if not args.tag:
            args.tag = _config.tag.keys()
        for tag in args.tag:
            if (
                args.group_id in _config.group
                and tag in _config.group[args.group_id].subscribe
            ):
                _config.group[args.group_id].subscribe.remove(tag)
        _config.dump()

    @classmethod
    async def set(cls, args: Namespace) -> str:
        try:
            await get_latest_notice(args.api_server, "main")
            _config.api_server = args.api_server
            _config.dump()
            message = "成功设置通知 API 服务器！"
        except:
            message = "服务器未通过检测，设置失败！"
        return message
