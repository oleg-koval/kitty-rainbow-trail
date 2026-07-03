"""Side-effecting boundary: talks to a running kitty instance over its remote-control socket.

Isolated here so `color_wheel.py` and the orchestration in `cli.py` stay pure/testable.
"""

import subprocess
from pathlib import Path

OVERRIDE_FILENAME = "rainbow-trail-override.conf"


class RemoteControlError(RuntimeError):
    """Raised when kitty's remote-control socket can't be reached."""


def override_path(config_dir: Path) -> Path:
    """Path to the conf snippet that `kitty.conf` includes for the live trail color."""
    return config_dir / OVERRIDE_FILENAME


def write_trail_color(config_dir: Path, color: str) -> None:
    """Write the current trail color into the included override conf file."""
    override_path(config_dir).write_text(f"cursor_trail_color {color}\n")


def reload_config(to: str | None = None) -> None:
    """Ask the running kitty instance to hot-reload its config via `kitty @ load-config`.

    Raises RemoteControlError if `allow_remote_control` isn't enabled in kitty.conf,
    since that's the single most common setup mistake for this feature.
    """
    command = ["kitty", "@"]
    if to:
        command += ["--to", to]
    command += ["load-config"]

    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RemoteControlError(
            "kitty @ load-config failed - is `allow_remote_control socket-only` "
            f"(and `listen_on`) set in kitty.conf? stderr: {result.stderr.strip()}"
        )
