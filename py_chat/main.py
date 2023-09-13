import argparse
from collections.abc import Sequence
from typing import Union

from py_chat.client import start
from py_chat.server import serve


def main(argv: Union[Sequence[str], None] = None) -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-s", "--server", help="Start server", action="store_true"
    )
    group.add_argument(
        "-c", "--client", help="Start client", action="store_true"
    )
    args: argparse.Namespace = parser.parse_args(argv)

    if args.server:
        serve()
    elif args.client:
        start()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
