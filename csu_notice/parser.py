from nonebot.rule import ArgumentParser

_parser = ArgumentParser("csu_notice")

subparsers = _parser.add_subparsers(dest="handle")

sub = subparsers.add_parser("sub")
sub.add_argument("tag", nargs="*")

unsub = subparsers.add_parser("unsub")
unsub.add_argument("tag", nargs="*")

set = subparsers.add_parser("set")
set.add_argument("name")
set.add_argument("value")

srch = subparsers.add_parser("srch")
srch.add_argument("title")
srch.add_argument("-T", "--tag", default="main")

show = subparsers.add_parser("show")
show.add_argument("id", nargs="?", default=0)
show.add_argument("-T", "--tag", default="main")

rl = subparsers.add_parser("rl")
rl.add_argument("id")
rl.add_argument("-T", "--tag", default="main")

fl = subparsers.add_parser("fl")
fl.add_argument("-f", "--from", action="store", nargs="*", default=[], type=str)
fl.add_argument("-k", "--keyword", action="store", nargs="*", default=[], type=str)
fl.add_argument("-r", "--remove", action="store_true")
fl.add_argument("-O", "--filter-out", action="store_true")
