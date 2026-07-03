# AGENTS.md

Instructions for AI coding agents (Claude Code, Codex, Cursor, Copilot).

## Setup

This project uses [uv](https://docs.astral.sh/uv/). If `uv` is not installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then:

```bash
uv sync
```

## Commands

- Run tests: `uv run pytest`
- Lint + auto-fix: `uv run ruff check --fix`
- Format: `uv run ruff format`
- Type-check: `uv run ty check`

Run all four before submitting a PR. CI runs the same commands.

## Pre-commit hooks

Requires `pre-commit` (included in dev deps). Install once after `uv sync`:

```bash
make hooks
```

Hooks run ruff lint + format, ty check, pytest, and a 300-line file-length check
on every commit. `git commit --no-verify` is rejected in code review.

## Conventions

- Python 3.12+. Use modern syntax: `match`, PEP 695 generics, `|` unions.
- Type-hint all public functions. Internal helpers may skip if obvious.
- Docstrings on public APIs only. Style: short imperative summary line.
- Tests live in `tests/`, mirror `src/` layout, use plain `assert`.
  Prefer integration/E2E tests that exercise the public interface end-to-end.
  Unit-test only pure functions with non-trivial branching (`color_wheel.py`).
- Keep side effects confined to `kitty_remote.py`. `color_wheel.py` must stay pure.
- No new top-level dependencies without discussion. Dev deps go in
  `dependency-groups.dev`.

## Don't

- Don't add `# type: ignore` without a comment explaining why.
- Don't commit without `ruff check`, `ruff format`, and `ty check` passing.
- Don't introduce sync I/O in async paths or vice versa.
- Don't add mocked-only tests for `kitty_remote.py` - use the fake-kitty-on-PATH
  pattern in `tests/test_cli_e2e.py` so the real subprocess path is exercised.
