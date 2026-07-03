"""Pure logic, kept separate from the remote-control side effect in kitty_remote.py."""


def greet(name: str = "world") -> str:
    """Return a friendly, kitty-themed greeting."""
    return f"Meow, {name}!"
