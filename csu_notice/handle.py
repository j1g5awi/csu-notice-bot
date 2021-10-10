from argparse import Namespace
from typing import Optional

from .config import _config, Group
from .data_source import get_latest_notice
from csu_notice import config


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
        if not _config.group[args.group_id].subscribe:
            _config.group.pop(args.group_id)
        _config.dump()

    @classmethod
    async def set(cls, args: Namespace) -> Optional[str]:
        try:
            await get_latest_notice(args.api_server, "main")
            _config.api_server = args.api_server
            _config.dump()
        except:
            return "服务器未通过检测，设置失败！"

    @classmethod
    async def fl(cls, args: Namespace) -> Optional[str]:
        if args.group_id not in _config.group:
            return "本群未订阅任何校内通知，请先订阅！"
        filter = "filter_out" if args.filter_out else "filter"
        if not args.remove:
            for from_ in getattr(args, "from"):
                if from_ not in getattr(_config.group[args.group_id], filter).from_:
                    getattr(_config.group[args.group_id], filter).from_.append(from_)
            for key_word in args.keyword:
                if key_word not in getattr(_config.group[args.group_id], filter).from_:
                    getattr(_config.group[args.group_id], filter).keyword.append(
                        key_word
                    )
        else:
            for from_ in getattr(args, "from"):
                if from_ in getattr(_config.group[args.group_id], filter).from_:
                    getattr(_config.group[args.group_id], filter).from_.remove(from_)
            for key_word in args.keyword:
                if key_word in getattr(_config.group[args.group_id], filter).from_:
                    getattr(_config.group[args.group_id], filter).keyword.remove(
                        key_word
                    )
        _config.dump()
