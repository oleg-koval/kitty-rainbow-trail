"""Pure hue-cycling math: elapsed time -> a hex color on the rainbow wheel."""

import colorsys

FULL_HUE_DEGREES = 360.0


def hue_at(elapsed_seconds: float, degrees_per_second: float) -> float:
    """Return the current hue in degrees [0, 360) for a given elapsed time."""
    return (elapsed_seconds * degrees_per_second) % FULL_HUE_DEGREES


def hue_to_hex(hue_degrees: float, saturation: float = 1.0, value: float = 1.0) -> str:
    """Convert an HSV hue (degrees) to a "#rrggbb" hex string.

    HSV at full saturation/value is used instead of interpolating RGB directly
    because it produces a perceptually even sweep through the spectrum with no
    dark or muddy transitions between primary colors.
    """
    red, green, blue = colorsys.hsv_to_rgb(hue_degrees / FULL_HUE_DEGREES, saturation, value)
    return f"#{round(red * 255):02x}{round(green * 255):02x}{round(blue * 255):02x}"


def color_at(elapsed_seconds: float, degrees_per_second: float) -> str:
    """Return the trail color for a given elapsed time and cycle speed."""
    return hue_to_hex(hue_at(elapsed_seconds, degrees_per_second))
