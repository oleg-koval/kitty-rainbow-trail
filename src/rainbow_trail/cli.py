"""`rainbow-trail` entrypoint: cycles kitty's cursor_trail_color through the rainbow.

Usage:
    rainbow-trail start   [--speed DEG/S] [--interval SECONDS] [--to SOCKET]
    rainbow-trail stop
    rainbow-trail toggle  [--speed DEG/S] [--interval SECONDS] [--to SOCKET]
"""

import argparse
import os
import signal
import subprocess
import sys
import time
from collections.abc import Callable
from pathlib import Path

from rainbow_trail import kitty_remote
from rainbow_trail.color_wheel import color_at

DEFAULT_SPEED_DEGREES_PER_SECOND = 30.0
DEFAULT_INTERVAL_SECONDS = 0.05
DEFAULT_STATIC_COLOR = "none"
PID_FILENAME = "rainbow-trail.pid"


def default_config_dir() -> Path:
    return Path(os.environ.get("KITTY_CONFIG_DIRECTORY", Path.home() / ".config" / "kitty"))


def pid_path(config_dir: Path) -> Path:
    return config_dir / PID_FILENAME


def running_pid(config_dir: Path) -> int | None:
    """Return the pid in the pidfile if that process is still alive, else None."""
    path = pid_path(config_dir)
    if not path.exists():
        return None
    try:
        pid = int(path.read_text().strip())
        os.kill(pid, 0)
    except (ValueError, ProcessLookupError, PermissionError):
        path.unlink(missing_ok=True)
        return None
    return pid


def _always_continue() -> bool:
    return True


class CycleClock:
    """Injectable time sources for `run_cycle`, so tests avoid real wall-clock waits."""

    def __init__(
        self,
        now: Callable[[], float] = time.monotonic,
        sleep: Callable[[float], None] = time.sleep,
        should_continue: Callable[[], bool] = _always_continue,
    ) -> None:
        self.now = now
        self.sleep = sleep
        self.should_continue = should_continue


def run_cycle(
    config_dir: Path,
    speed: float,
    interval: float,
    to: str | None,
    clock: CycleClock | None = None,
) -> None:
    """Foreground loop: write + reload a new rainbow color every `interval` seconds."""
    clock = clock or CycleClock()
    start = clock.now()
    while clock.should_continue():
        color = color_at(elapsed_seconds=clock.now() - start, degrees_per_second=speed)
        kitty_remote.write_trail_color(config_dir, color)
        kitty_remote.reload_config(to=to)
        clock.sleep(interval)


def start(config_dir: Path, speed: float, interval: float, to: str | None) -> None:
    if running_pid(config_dir) is not None:
        print("rainbow-trail is already running (use `rainbow-trail stop` first).")
        return

    pid_path(config_dir).write_text(str(os.getpid()))
    stop_requested = False

    def request_stop(_signum: int, _frame: object) -> None:
        nonlocal stop_requested
        stop_requested = True

    signal.signal(signal.SIGTERM, request_stop)
    clock = CycleClock(should_continue=lambda: not stop_requested)
    try:
        run_cycle(config_dir, speed, interval, to, clock)
    finally:
        kitty_remote.write_trail_color(config_dir, DEFAULT_STATIC_COLOR)
        kitty_remote.reload_config(to=to)
        pid_path(config_dir).unlink(missing_ok=True)


def stop(config_dir: Path) -> None:
    pid = running_pid(config_dir)
    if pid is None:
        print("rainbow-trail is not running.")
        return
    os.kill(pid, signal.SIGTERM)


def toggle(config_dir: Path, speed: float, interval: float, to: str | None) -> None:
    if running_pid(config_dir) is not None:
        stop(config_dir)
        return

    command = [
        sys.executable,
        "-m",
        "rainbow_trail.cli",
        "start",
        "--speed",
        str(speed),
        "--interval",
        str(interval),
        *(["--to", to] if to else []),
    ]
    subprocess.Popen(
        command,
        start_new_session=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="rainbow-trail")
    parser.add_argument(
        "--config-dir",
        type=Path,
        default=None,
        help="kitty config dir (default: $KITTY_CONFIG_DIRECTORY or ~/.config/kitty)",
    )
    parser.add_argument("--speed", type=float, default=DEFAULT_SPEED_DEGREES_PER_SECOND)
    parser.add_argument("--interval", type=float, default=DEFAULT_INTERVAL_SECONDS)
    parser.add_argument(
        "--to",
        type=str,
        default=None,
        help="kitty remote-control target, e.g. unix:/tmp/kitty.sock",
    )
    parser.add_argument("command", choices=["start", "stop", "toggle"])
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config_dir = args.config_dir or default_config_dir()

    try:
        if args.command == "start":
            start(config_dir, args.speed, args.interval, args.to)
        elif args.command == "stop":
            stop(config_dir)
        else:
            toggle(config_dir, args.speed, args.interval, args.to)
    except kitty_remote.RemoteControlError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
