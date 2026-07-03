# Contributing

## Workflow

1. Fork and branch from `main`.
2. `uv sync` to install dev deps.
3. Make changes. Run `uv run ruff check --fix && uv run ruff format && uv run ty check && uv run pytest`.
4. Open a PR with a clear description and motivation.

## Issues

Bug reports: include reproduction steps, expected vs actual behavior, kitty version, and OS.
Feature requests: describe the use case before the proposed API.

## Commit messages

Conventional Commits: `feat:`, `fix:`, `docs:`, `chore:`, etc.
Breaking changes get `!`: `feat!: drop Python 3.11 support`.
