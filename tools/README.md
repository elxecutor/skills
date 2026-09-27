# tools

Three skills in this collection depend on programs that live outside the repository.
One of those programs is a small script kept here. The other two have to be installed
separately.

| Skill | Needs | Provided here |
| --- | --- | --- |
| [`claude`](../claude/SKILL.md) | `claude-cli` | [`claude-cli`](claude-cli) |
| [`herdr`](../herdr/SKILL.md) | the `herdr` binary | no — install it |
| [`acquaint`](../acquaint/SKILL.md) | an `AGENTS.md` | no — yours to write |

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
