from nonebot.rule import ArgumentParser

_parser = ArgumentParser("csu_notice")

subparsers = _parser.add_subparsers(dest="handle")

sub = subparsers.add_parser("sub")
sub.add_argument("tag", nargs="*")

unsub = subparsers.add_parser("unsub")
unsub.add_argument("tag", nargs="*")

set = subparsers.add_parser("set")
set.add_argument("api_server")

fl = subparsers.add_parser("fl")
fl.add_argument("-f", "--from", action="store", nargs="*", default=[], type=str)
fl.add_argument("-k", "--keyword", action="store", nargs="*", default=[], type=str)
fl.add_argument("-r", "--remove", action="store_true")
fl.add_argument("-O", "--filter-out", action="store_true")