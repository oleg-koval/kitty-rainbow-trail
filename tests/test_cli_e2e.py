"""End-to-end test against the real CLI entrypoint, using a fake `kitty` on PATH.

A real kitty terminal isn't available in CI, but everything past the process boundary
(subprocess invocation, argument parsing) is exercised for real - only the kitty binary
itself is a test double. Copy this pattern for your own kitten's E2E tests.
"""

import stat
from pathlib import Path

import pytest

from kitty_starter.cli import main


@pytest.fixture
def fake_kitty_on_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A stub `kitty` executable whose `@` subcommands always succeed."""
    import os

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake_kitty = bin_dir / "kitty"
    fake_kitty.write_text("#!/bin/sh\nexit 0\n")
    fake_kitty.chmod(fake_kitty.stat().st_mode | stat.S_IEXEC)
    monkeypatch.setenv("PATH", f"{bin_dir}:{os.environ.get('PATH', '')}")
    return bin_dir


def test_ping_prints_greeting(fake_kitty_on_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main(["ping", "--name", "Oleg"])

    assert exit_code == 0
    assert capsys.readouterr().out.strip() == "Meow, Oleg!"


def test_ping_fails_loudly_without_remote_control(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("PATH", str(tmp_path))  # no `kitty` binary on PATH

    exit_code = main(["ping"])

    assert exit_code == 1
    assert "error:" in capsys.readouterr().err
