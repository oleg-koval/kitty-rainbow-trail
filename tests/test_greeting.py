from kitty_starter.greeting import greet


def test_greet_default() -> None:
    assert greet() == "Meow, world!"


def test_greet_named() -> None:
    assert greet("Oleg") == "Meow, Oleg!"
