.PHONY: lint format typecheck test hooks ci

lint:
	uv run ruff check --fix

format:
	uv run ruff format

typecheck:
	uv run ty check

test:
	uv run pytest

hooks:
	uv run pre-commit install

ci: lint format typecheck test
