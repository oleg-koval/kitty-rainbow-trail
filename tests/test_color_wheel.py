import re

from rainbow_trail.color_wheel import color_at, hue_at, hue_to_hex

HEX_COLOR_RE = re.compile(r"^#[0-9a-f]{6}$")


def test_hue_at_wraps_at_360_degrees() -> None:
    assert hue_at(elapsed_seconds=1.0, degrees_per_second=360.0) == 0.0


def test_hue_at_advances_linearly() -> None:
    expected_hue_degrees = 30.0
    assert hue_at(elapsed_seconds=0.5, degrees_per_second=60.0) == expected_hue_degrees


def test_hue_to_hex_red_at_zero_degrees() -> None:
    assert hue_to_hex(0.0) == "#ff0000"


def test_hue_to_hex_green_at_120_degrees() -> None:
    assert hue_to_hex(120.0) == "#00ff00"


def test_hue_to_hex_blue_at_240_degrees() -> None:
    assert hue_to_hex(240.0) == "#0000ff"


def test_color_at_returns_valid_hex_string() -> None:
    assert HEX_COLOR_RE.match(color_at(elapsed_seconds=3.7, degrees_per_second=15.0))


def test_color_at_is_pure_and_deterministic() -> None:
    first = color_at(elapsed_seconds=2.0, degrees_per_second=10.0)
    second = color_at(elapsed_seconds=2.0, degrees_per_second=10.0)
    assert first == second


def test_color_at_cycles_back_to_start_after_full_rotation() -> None:
    start = color_at(elapsed_seconds=0.0, degrees_per_second=36.0)
    after_full_rotation = color_at(elapsed_seconds=10.0, degrees_per_second=36.0)
    assert start == after_full_rotation
