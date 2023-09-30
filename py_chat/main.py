import argparse
import curses
from collections.abc import Sequence
from typing import Union

from py_chat.client import c_main
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
    parser.add_argument(
        "--color",
        help="Use the terminal's default colors (Only works with `--client`)",
        action="store_true",
    )

    args: argparse.Namespace = parser.parse_args(argv)

    if args.server:
        serve()
    elif args.client:
        return curses.wrapper(c_main, args.color)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
