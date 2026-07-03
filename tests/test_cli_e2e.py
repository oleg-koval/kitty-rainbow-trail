"""End-to-end tests against the real CLI entrypoint, using a fake `kitty` on PATH.

A real kitty terminal isn't available in CI, but everything past the process
boundary (subprocess invocation, pidfile lifecycle, file writes) is exercised
for real - only the kitty binary itself is a test double.
"""

import os
import stat
import subprocess
import sys
import time
from pathlib import Path

import pytest

from rainbow_trail.cli import CycleClock, pid_path, run_cycle
from rainbow_trail.kitty_remote import override_path


@pytest.fixture
def fake_kitty_on_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A stub `kitty` executable whose `@ load-config` subcommand always succeeds."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake_kitty = bin_dir / "kitty"
    fake_kitty.write_text("#!/bin/sh\nexit 0\n")
    fake_kitty.chmod(fake_kitty.stat().st_mode | stat.S_IEXEC)
    monkeypatch.setenv("PATH", f"{bin_dir}:{os.environ.get('PATH', '')}")
    return bin_dir


def test_run_cycle_writes_distinct_colors_across_iterations(
    tmp_path: Path, fake_kitty_on_path: Path
) -> None:
    config_dir = tmp_path / "kitty-config"
    config_dir.mkdir()
    fake_clock = iter([0.0, 1.0, 2.0, 3.0])
    seen_colors: list[str] = []
    iterations_remaining = 3

    def record_and_continue() -> bool:
        nonlocal iterations_remaining
        if override_path(config_dir).exists():
            seen_colors.append(override_path(config_dir).read_text())
        iterations_remaining -= 1
        return iterations_remaining >= 0

    run_cycle(
        config_dir,
        speed=90.0,
        interval=0.0,
        to=None,
        clock=CycleClock(
            now=lambda: next(fake_clock),
            sleep=lambda _seconds: None,
            should_continue=record_and_continue,
        ),
    )

    assert len(set(seen_colors)) > 1, "expected the trail color to change between iterations"


def test_start_then_stop_via_real_subprocess(tmp_path: Path, fake_kitty_on_path: Path) -> None:
    config_dir = tmp_path / "kitty-config"
    config_dir.mkdir()

    timeout_seconds = 5
    command = [
        sys.executable,
        "-m",
        "rainbow_trail.cli",
        "start",
        "--config-dir",
        str(config_dir),
        "--interval",
        "0.01",
    ]
    process = subprocess.Popen(command)
    try:
        deadline = time.monotonic() + timeout_seconds
        while not pid_path(config_dir).exists() and time.monotonic() < deadline:
            time.sleep(0.05)
        assert pid_path(config_dir).exists(), "expected pidfile to appear once started"

        subprocess.run(
            [sys.executable, "-m", "rainbow_trail.cli", "stop", "--config-dir", str(config_dir)],
            check=True,
        )
        process.wait(timeout=timeout_seconds)
    finally:
        if process.poll() is None:
            process.kill()

    assert not pid_path(config_dir).exists(), "expected pidfile to be cleaned up on stop"
    assert override_path(config_dir).read_text() == "cursor_trail_color none\n"
