# kitty-starter

> A minimal, generalized template for kitty terminal customizations - kittens, remote-control
> tools, and documented `kitty.conf` snippets.

[![CI](https://github.com/oleg-koval/kitty-starter/actions/workflows/ci.yml/badge.svg)](https://github.com/oleg-koval/kitty-starter/actions/workflows/ci.yml)

This is a **template repo**, not a finished tool. Click "Use this template" on GitHub (or
`gh repo create my-thing --template oleg-koval/kitty-starter`) to start a new kitty customization
project with governance files, CI, and tooling already wired up.

## What's included

- `kitty.conf` — boilerplate for enabling remote control and the `include`-based hot-reload
  pattern most kitty tooling needs, documented line by line.
- `src/kitty_starter/` — a trivial worked example (`ping`) showing the pattern to follow: pure
  logic (`greeting.py`) kept separate from the one module that talks to kitty
  (`kitty_remote.py`), wired together in `cli.py`.
- Tests for both layers: unit tests for the pure function, an end-to-end test against the real
  CLI using a fake `kitty` binary on `PATH` (kitty itself isn't available in CI).
- uv + ruff + ty tooling, pre-commit hooks, GitHub Actions CI, and the standard governance files
  (LICENSE, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, CHANGELOG, AGENTS.md).

## Using this template

```bash
gh repo create my-kitty-tool --template oleg-koval/kitty-starter --public --clone
cd my-kitty-tool
uv sync
```

Then:
1. Rename `src/kitty_starter/` to your project's package name and update `pyproject.toml`
   (`name`, `[project.scripts]`, `[tool.hatch.build.targets.wheel]`).
2. Replace `greeting.py` / `cli.py`'s `ping` command with your actual feature - keep the pure vs.
   remote-control split.
3. Replace the placeholder `kitty.conf` comments with the settings your project actually needs.
4. Update the README, CHANGELOG, and pyproject description for your project.

## Example: the `ping` command

```bash
uv run kitty-starter ping --name Oleg
```

Sets the current kitty window's title to `Meow, Oleg!` via `kitty @ set-window-title`, and prints
the same message. It exists only to demonstrate the pattern above - delete it once you've replaced
it with your own command.

## System Requirements

- kitty >= 0.28 (for remote control via `allow_remote_control` / `listen_on`)
- Python >= 3.12

## Architecture

- `greeting.py` — pure function, zero I/O, fully unit tested.
- `kitty_remote.py` — the only side-effecting module: wraps `kitty @ ...` calls.
- `cli.py` — orchestrates the two above. Follow this split for your own kitten.

## Security Notes

The remote-control socket (`listen_on unix:/tmp/kitty-starter`) is local-only (a Unix domain
socket) and `socket-only` scopes control to that socket specifically. See
[SECURITY.md](./SECURITY.md).

## Development

Requires [uv](https://docs.astral.sh/uv/) (one-time install):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # macOS / Linux
# or: brew install uv
```

Then:

```bash
uv sync                  # install deps + create .venv
uv run pytest            # run tests
uv run ruff check --fix  # lint
uv run ruff format       # format
uv run ty check          # type-check
```

## Contributing

PRs welcome. See [CONTRIBUTING.md](./CONTRIBUTING.md), [AGENTS.md](./AGENTS.md), and
[CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md).

## Other starters

Part of a set with shared conventions (AGENTS.md, Conventional Commits, MIT, GitHub Actions CI, Dependabot):

- [`ts-npm-starter`](https://github.com/oleg-koval/ts-npm-starter) - TypeScript / Node
- [`py-starter`](https://github.com/oleg-koval/py-starter) - Python (uv + ruff + ty)
- [`go-starter`](https://github.com/oleg-koval/go-starter) - Go (standard layout + golangci-lint)
- [`kitty-starter`](https://github.com/oleg-koval/kitty-starter) - kitty terminal customizations - this repo

## License

MIT - see [LICENSE](./LICENSE).

## Author

[Oleg Koval](https://github.com/oleg-koval)
