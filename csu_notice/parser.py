from nonebot.rule import ArgumentParser

_parser = ArgumentParser("csu_notice")

subparsers = _parser.add_subparsers(dest="handle")

sub = subparsers.add_parser("sub")
sub.add_argument("tag", nargs="*")

unsub = subparsers.add_parser("unsub")
unsub.add_argument("tag", nargs="*")

set = subparsers.add_parser("set")
set.add_argument("api_server")
