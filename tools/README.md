# tools

Four skills in this collection wrap programs that live outside the repository. Two
of those programs are small scripts kept here. The other two are third-party and
have to be installed.

| Skill | Needs | Provided here |
| --- | --- | --- |
| [`browser-use`](../browser-use/SKILL.md) | `bu` and `browser-harness` | [`bu`](bu) only |
| [`claude`](../claude/SKILL.md) | `claude-cli` | [`claude-cli`](claude-cli) |
| [`herdr`](../herdr/SKILL.md) | the `herdr` binary | no — install it |
| [`acquaint`](../acquaint/SKILL.md) | an `AGENTS.md` | no — yours to write |

## bu

A nine-line shell wrapper. It reads Brave's `DevToolsActivePort` file to discover the
live debugger endpoint, exports it as `BU_CDP_WS`, and hands off to `browser-harness`.
The indirection exists so a skill never has to guess which port the browser picked.

```bash
install -m 755 tools/bu ~/.local/bin/bu
```

It sources `~/.local/bin/env`, so that file has to exist.

## claude-cli

Talks to Claude.ai over HTTP from the command line — list, read, create, rename,
delete conversations, and hold a back-and-forth until a conclusion is reached. No API
key; it authenticates with a browser cookie.

```bash
install -m 755 tools/claude-cli ~/.local/bin/claude-cli
claude-cli --update-cookie
```

The `--update-cookie` step is interactive: it prints the cookies it needs
(`sessionKey`, `cf_clearance`, `anthropic-device-id`, `lastActiveOrg`) for you to copy
out of your signed-in browser, then writes them to
`~/.config/opencode/claude-cookie`. No credential is stored in this repository —
only the names of the cookies the tool reads.

## browser-harness

Not in this repository. It is a published Python package, and the `browser-harness`
file you may already have at `~/.local/bin/` is a shim that uv generates — it hardcodes
the absolute path of its own virtualenv, which is why it is not portable and not
committed here. Install the package and uv writes an equivalent shim for you:

```bash
uv tool install browser-harness   # tested against 0.1.13, requires Python >= 3.11
```

## herdr

Not in this repository — a ~26 MB compiled binary. Obtain a release for your platform
and put it on your `PATH`:

```bash
# tested against 0.9.1 on linux-x86_64
curl -fsSL -o ~/.local/bin/herdr \
  https://github.com/herdrdev/herdr/releases/download/v0.9.1/herdr-linux-x86_64
chmod +x ~/.local/bin/herdr
```

Project documentation lives at <https://herdr.dev/>. The `herdr` skill only does
anything inside a session Herdr is already managing, so it also checks for `HERDR_ENV=1`
before issuing any command.
