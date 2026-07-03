# Security Policy

## Supported Versions

| Version      | Supported           |
| ------------ | ------------------- |
| Latest minor | Yes                 |
| Older        | No                  |

## About the remote-control socket

Tools built from this template use `allow_remote_control socket-only` and a
`listen_on unix:/tmp/...` socket in `kitty.conf`. This is a local Unix domain socket scoped to
your user, not a network listener - only local processes running as you can reach it.
`socket-only` (rather than `yes`) additionally restricts control to that socket, so other kitty
windows/tabs on the same machine can't issue arbitrary remote-control commands to this instance
over a different transport.

## Reporting a Vulnerability

**Please do not open a public GitHub issue for security vulnerabilities.**

Email **kvl.olg@gmail.com** with:

1. A description of the vulnerability and its potential impact
2. Steps to reproduce or a proof-of-concept
3. Any suggested fixes (optional but appreciated)

You will receive an acknowledgement within 48 hours and a resolution timeline within 7 days.
