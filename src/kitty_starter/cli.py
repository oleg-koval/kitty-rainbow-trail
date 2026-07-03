"""`kitty-starter` entrypoint: a trivial example wiring pure logic to a remote-control call.

Replace `ping` with your own kitten's commands - the pattern (pure logic in one module,
`kitty @ ...` calls isolated in `kitty_remote.py`, orchestration here) is the point.
"""

import argparse
import sys

from kitty_starter import kitty_remote
from kitty_starter.greeting import greet


def ping(name: str, to: str | None) -> str:
    """Set the active kitty window's title to a greeting, return what was sent."""
    message = greet(name)
    kitty_remote.run("set-window-title", message, to=to)
    return message


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="kitty-starter")
    parser.add_argument("--name", default="world")
    parser.add_argument(
        "--to", default=None, help="kitty remote-control target, e.g. unix:/tmp/kitty.sock"
    )
    parser.add_argument("command", choices=["ping"])
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        message = ping(args.name, args.to)
    except kitty_remote.RemoteControlError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    print(message)
    return 0


if __name__ == "__main__":
    sys.exit(main())
