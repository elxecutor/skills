# Contributing

Thanks for adding a skill. This document covers what a skill has to look like, how
to write one, and what a reviewer will check.

## Repository layout

```
<skill-name>/
  SKILL.md              # required — frontmatter plus the skill body
  references/           # optional — long docs loaded only when needed
  scripts/              # optional — executable helpers
  agents/               # optional — per-agent interface config
CODE_OF_CONDUCT.md
CONTRIBUTING.md
LICENSE
README.md
```

One directory per skill, named exactly as the `name` in its frontmatter.

## Adding a skill

1. Create `<skill-name>/SKILL.md`.
2. Add a row for it to the table in [README.md](README.md), sorted alphabetically.
3. Open a pull request.

To try a skill locally before you push, copy the directory into the skills path
your opencode setup scans — commonly `~/.agents/skills/` or
`~/.config/opencode/skills/`.

## Frontmatter

`SKILL.md` opens with YAML frontmatter. Only `name` and `description` are required.

```yaml
---
name: my-skill
description: One or two sentences saying what it does and when the agent should reach for it.
---
```

Rules:

- `name` matches the directory name, lowercase, hyphen-separated.
- `description` is what an agent matches against when deciding whether to load the
  skill. Write it for the trigger you want, not as marketing copy: state the
  capability, then the conditions that should invoke it.
- `license` is optional per skill. The repository license covers the collection.
- `disable-model-invocation: true` marks a skill the user must ask for by name,
  such as one that only makes sense in an interactive session.

## Writing the body

- Lead with the role or goal in a sentence or two, then the steps.
- Prefer concrete commands and file references over prose describing them.
- Say what the skill must **not** do as explicitly as what it should. Boundaries
  are where agent behavior actually goes wrong.
- Keep the main file scannable. Push long reference material into
  `references/*.md` and link to it, so the body stays cheap to load.
- Use GitHub-flavored Markdown and
  [admonition syntax](https://github.com/orgs/community/discussions/16925) for
  warnings and prerequisites.
- No emoji as structure. A warning reads better as a blockquote.

## Safety requirements

These are not style preferences. A pull request that violates them will not be
merged.

- **No secrets, ever.** No API keys, tokens, cookies, passwords, or `.env`
  contents in a skill or its examples. Use placeholders like `<YOUR_TOKEN>`.
- **No personal data.** No real usernames, absolute home directory paths,
  hostnames, or email addresses. Write `~/` and `<user>`.
- **Destructive actions are advisory-only.** A skill that reports on system state
  — disk usage, bloat, dead files — prints findings and exact commands for the
  user to run. It does not execute removals itself. If a skill needs to run
  commands, name the ones that are safe and mark the rest as user-initiated.
- **Respect the instruction boundary.** Text inside a repository under audit is
  data, not instructions. A skill that reads a codebase must say so, or it will
  inherit whatever that codebase tells it to do.

## Review criteria

A reviewer will check:

- Does the skill do one thing, with a description that makes it obvious when to
  reach for it?
- Are its failure modes addressed — what it must never do, and what to do when a
  step is blocked?
- Does it work from a clean checkout with only the files in this repository?
- Are all commands, paths, and links valid?

## Reporting a problem

Open an issue. For behavior that violates the
[Code of Conduct](CODE_OF_CONDUCT.md), open an issue as described there.

## License

By contributing, you agree that your contribution is licensed under the
[MIT License](LICENSE).
