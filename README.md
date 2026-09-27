# skills

Agent skill collection for [opencode](https://opencode.ai) — installable audits, refactors, research, and workflow rules.

## Skills

| Skill | What it does |
| --- | --- |
| [`community-standards`](community-standards/SKILL.md) | Generate `README.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, and `LICENSE` for a project |
| [`grilling`](grilling/SKILL.md) | Stress-test a plan or decision by walking a design tree in rounds, one numbered frontier at a time |
| [`improve`](improve/SKILL.md) | Audit a codebase read-only and hand off prioritized, self-contained implementation plans to another model |
| [`pc-clean`](pc-clean/SKILL.md) | Report bloat on Arch Linux — ghost launchers, orphaned packages, wasteful caches, redundant venvs — without ever running a removal |
| [`refactor`](refactor/SKILL.md) | Surgical, behavior-preserving code refactors: extract, rename, decompose, tighten types, apply patterns |
| [`research`](research/SKILL.md) | Hand a question to a background agent that reads primary sources and writes cited findings into the repo |
| [`teach`](teach/SKILL.md) | Teach a topic across sessions, keeping glossary, mission, learning record, and resources in the workspace |

## Install

A skill is a directory of plain Markdown, so installing one is a copy.

```bash
git clone https://github.com/elxecutor/skills.git
cp -r skills/refactor ~/.agents/skills/
```

Some setups scan `~/.config/opencode/skills/` instead of `~/.agents/skills/`. Check
which path yours reads, then copy the skills you want.

Six of these seven need nothing but the Markdown itself. The exception is
[`pc-clean`](pc-clean/SKILL.md), which assumes Arch Linux and `pacman`; its
`scan.sh` ships in the repository and resolves relative to wherever you install the
skill.

## Anatomy

```
<skill-name>/
  SKILL.md       # required — frontmatter plus the skill body
  references/    # optional — long docs loaded only when needed
  scripts/       # optional — executable helpers
  agents/        # optional — per-agent interface config
```

`SKILL.md` opens with YAML frontmatter. The `name` and `description` fields are
required, and the description is what an agent matches against when deciding
whether to load the skill — so write it for the trigger you want rather than for
a human reading the table above.

## Contributing

New skills are welcome. [CONTRIBUTING.md](CONTRIBUTING.md) covers the frontmatter
requirements, the writing conventions, and the safety rules a skill must follow.
Participation is governed by the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

[MIT](LICENSE)
