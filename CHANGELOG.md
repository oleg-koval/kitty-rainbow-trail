# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Documented `cursor_trail` settings in `kitty.conf` for the flying/jumping cursor animation.
- `rainbow-trail` CLI (`rainbow_trail` package) that cycles `cursor_trail_color` through the hue
  wheel via kitty's remote-control API.
- `start` / `stop` / `toggle` commands with pidfile-based lifecycle management.
- Unit tests for the pure hue-cycling math and end-to-end tests against the real CLI.
