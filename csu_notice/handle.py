from argparse import Namespace
from typing import Optional

from .utils import format_notice
from .config import _config, Group
from .data_source import get_latest_head, reload_content, search_notice, get_notice


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
        if args.name == "api_server":
            try:
                await get_latest_head(args.value, "main")
                _config.api_server = args.value
                _config.dump()
            except:
                return "服务器未通过检测！"
        elif args.name == "token":
            if _config.api_server:
                try:
                    assert await reload_content(
                        _config.api_server, "main", "1", args.value
                    )
                    _config.token = args.value
                    _config.dump()
                except:
                    return "token 未通过检测！"
            else:
                return "请先设置服务器！"
        elif args.name == "limit":
            if args.value.isdigit():
                _config.limit = int(args.value)
                _config.dump()
            else:
                return "请设置为数字！"
        elif args.name == "enable_content":
            if args.value.lower() in ["true", "false"]:
                _config.enable_content = {"true": True, "false": False}[
                    args.value.lower()
                ]
                _config.dump()
            else:
                return "请设置为布尔值"
        else:
            return "该设置项不存在！"

    @classmethod
    async def srch(cls, args: Namespace) -> str:
        if _config.api_server:
            notices = await search_notice(_config.api_server, args.tag, args.title)
            return "\n".join(
                [
                    "｜".join([notice["title"], notice["from"], str(notice["id"])])
                    for notice in notices[-5:]
                ]
            )
        else:
            return "请设置 API 服务器！"

    @classmethod
    async def show(cls, args: Namespace) -> str:
        if _config.api_server:
            return format_notice(
                await get_notice(_config.api_server, args.tag, args.id), True
            )
        else:
            return "请设置 API 服务器！"

    @classmethod
    async def rl(cls, args: Namespace) -> Optional[str]:
        if _config.api_server:
            if _config.token:
                await reload_content(
                    _config.api_server, args.tag, args.id, _config.token
                )
            else:
                return "请设置 token！"
        else:
            return "请设置 API 服务器！"

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
