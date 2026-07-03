"""Side-effecting boundary: talks to a running kitty instance over its remote-control socket.

Isolated here so pure logic (see `greeting.py`) stays testable without a real kitty instance.
This is the pattern to copy for your own kitten: keep `kitty @ ...` calls in one small module,
everything else pure.
"""

import subprocess


class RemoteControlError(RuntimeError):
    """Raised when kitty's remote-control socket can't be reached."""


def run(*args: str, to: str | None = None) -> str:
    """Run `kitty @ <args>` and return its stdout.

    Raises RemoteControlError if `allow_remote_control` isn't enabled in kitty.conf,
    since that's the single most common setup mistake for remote-control tooling.
    """
    command = ["kitty", "@"]
    if to:
        command += ["--to", to]
    command += list(args)

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
    except FileNotFoundError as error:
        raise RemoteControlError("`kitty` binary not found on PATH") from error

    if result.returncode != 0:
        raise RemoteControlError(
            "kitty @ command failed - is `allow_remote_control socket-only` "
            f"(and `listen_on`) set in kitty.conf? stderr: {result.stderr.strip()}"
        )
    return result.stdout
