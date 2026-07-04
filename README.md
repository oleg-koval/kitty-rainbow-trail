<p align="center">
  <a href="https://github.com/oleg-koval/kitty-rainbow-trail/actions/workflows/ci.yml"><img src="https://github.com/oleg-koval/kitty-rainbow-trail/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/python-3.12%20%7C%203.13-blue.svg" alt="Python 3.12 | 3.13">
</p>

<p align="center">
  <img src="./logo.svg" width="120" height="120" alt="kitty-rainbow-trail icon: a terminal cursor block leading a rainbow comet trail">
</p>

<h1 align="center">kitty-rainbow-trail</h1>

<p align="center">
  A flying, jumping, rainbow-cycling cursor trail for the <a href="https://sw.kovidgoyal.net/kitty/">kitty</a> terminal<br>
  <strong>plus a documented <code>kitty.conf</code></strong>
</p>

---

## Features

- **Flying cursor trail** — kitty's built-in `cursor_trail` animation, pre-tuned and fully commented.
- **Rainbow cycling** — kitty only supports one static trail color; `rainbow-trail` sweeps it through
  the full hue wheel in real time by hot-reloading kitty's config several times a second.
- **Fully customizable** — every knob (speed, fade timing, hue speed, static color, on/off) is
  documented below with copy-paste examples.
- **Toggle keybinding** — flip the rainbow effect on/off with `ctrl+shift+r` out of the box.

## Installation

Requirements: [kitty](https://sw.kovidgoyal.net/kitty/binary/) 0.36 or newer and Python 3.12 or newer.

1. Install the `rainbow-trail` command from GitHub:

```bash
uv tool install git+https://github.com/oleg-koval/kitty-rainbow-trail
```

No `uv`? Use `pipx install git+https://github.com/oleg-koval/kitty-rainbow-trail` instead.

2. Download the trail settings as a separate config fragment. This preserves your existing
   `kitty.conf`:

```bash
mkdir -p ~/.config/kitty
curl -fsSL https://raw.githubusercontent.com/oleg-koval/kitty-rainbow-trail/main/kitty.conf \
  -o ~/.config/kitty/rainbow-trail.conf
printf '\ninclude rainbow-trail.conf\n' >> ~/.config/kitty/kitty.conf
```

If `include rainbow-trail.conf` is already present, do not add it a second time.

3. Restart kitty, then press `ctrl+shift+r`. The same shortcut stops the rainbow cycle.

To verify the command separately:

```bash
rainbow-trail toggle
```

## Existing clone

If you cloned this repository, install and configure it with:

```bash
uv tool install .
mkdir -p ~/.config/kitty
cp kitty.conf ~/.config/kitty/rainbow-trail.conf
printf '\ninclude rainbow-trail.conf\n' >> ~/.config/kitty/kitty.conf
```

## Troubleshooting

- `rainbow-trail: command not found`: ensure the uv or pipx tool bin directory is on `PATH`, then
  open a new shell. Run `uv tool dir --bin` to locate the uv directory.
- Nothing happens after the shortcut: restart kitty after adding the include; reloading only the
  current shell is not enough.
- `kitty @ load-config failed`: confirm `rainbow-trail.conf` is included and that no later config
  line overrides `allow_remote_control` or `listen_on`.

## Configuration

| Setting | Where | Effect |
|---|---|---|
| `cursor_trail <ms>` | `kitty.conf` | Stillness (ms) before the trail catches up. Lower = snappier. `0` disables the trail. |
| `cursor_trail_decay <in> <out>` | `kitty.conf` | Fade-in / fade-out timing in seconds. |
| `cursor_trail_start_threshold <cells>` | `kitty.conf` | Minimum cells moved before the trail animates; skips single-character typing. |
| `cursor_trail_color <hex\|none>` | `kitty.conf` | Static trail color used when rainbow mode is off. |
| `--speed <deg/s>` | `rainbow-trail` CLI | How fast the hue wheel spins. Default `30`. |
| `--interval <seconds>` | `rainbow-trail` CLI | How often the color updates. Default `0.05` (20fps). |
| `--to <socket>` | `rainbow-trail` CLI | kitty remote-control target, if not using the default `listen_on`. |

Disable the trail entirely: set `cursor_trail 0`. Disable only the rainbow cycling and keep a solid
color: run `rainbow-trail stop` and set `cursor_trail_color` to whatever hex value you like.

## Commands

```bash
rainbow-trail start                    # run the rainbow cycle in the foreground
rainbow-trail start --speed 90         # spin 3x faster
rainbow-trail start --interval 0.1     # update 10fps instead of 20fps
rainbow-trail stop                     # stop a running cycle, restore the static color
rainbow-trail toggle                   # start if stopped, stop if running (bound to ctrl+shift+r)
```

## System Requirements

- kitty >= 0.36 (for `cursor_trail`)
- Python >= 3.12
- `allow_remote_control` enabled in `kitty.conf` (shipped in this repo's `kitty.conf`)

## Architecture

- `color_wheel.py` — pure function: elapsed time + speed → hex color. Zero I/O, fully unit tested.
- `kitty_remote.py` — the only side-effecting module: writes the override conf file and calls
  `kitty @ load-config` over the remote-control socket.
- `cli.py` — orchestrates the two above in a loop, plus pidfile-based `start`/`stop`/`toggle`.

## Project Status

Early / actively developed. Not yet published to PyPI. See [CHANGELOG.md](./CHANGELOG.md).

## Security Notes

The remote-control socket (`listen_on unix:/tmp/kitty-rainbow-trail`) is local-only (a Unix domain
socket) and only accepts `load-config`-class commands from this kitten. See [SECURITY.md](./SECURITY.md).

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

## Built from

Generated from [`kitty-starter`](https://github.com/oleg-koval/kitty-starter), a minimal
generalized template for kitty terminal customizations.

## License

MIT - see [LICENSE](./LICENSE).

## Author

[Oleg Koval](https://github.com/oleg-koval)

---

<p align="center">
  <a href="https://github.com/oleg-koval/kitty-rainbow-trail">GitHub</a> ·
  <a href="./README.md">README</a> ·
  <a href="https://github.com/oleg-koval/kitty-rainbow-trail/releases">Releases</a> ·
  <a href="https://github.com/oleg-koval/kitty-rainbow-trail/issues">Issues</a>
</p>
