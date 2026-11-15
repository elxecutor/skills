# skills

Agent skill collection for [opencode](https://opencode.ai) — installable browser, research, productivity, and workflow skills.

## Skills

| Skill | What it does |
| --- | --- |
| [`acquaint`](acquaint/SKILL.md) | Read project instructions and extract actionable conventions, workflows, and constraints |
| [`browser-use`](browser-use/SKILL.md) | Control Chromium through CDP for interactive, authenticated, and Tor browser tasks |
| [`claude`](claude/SKILL.md) | Access Claude.ai conversations through the local `claude-cli` wrapper |
| [`community-standards`](community-standards/SKILL.md) | Generate `README.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, and `LICENSE` for a project |
| [`grilling`](grilling/SKILL.md) | Stress-test a plan or decision by walking a design tree in rounds, one numbered frontier at a time |
| [`improve`](improve/SKILL.md) | Audit a codebase read-only and hand off prioritized, self-contained implementation plans to another model |
| [`jiji`](jiji/SKILL.md) | Search and vet current Jiji Nigeria listings |
| [`jumia`](jumia/SKILL.md) | Search Jumia Nigeria through its public endpoints |
| [`kaggle`](kaggle/SKILL.md) | Run private Kaggle notebook jobs remotely and retrieve model artifacts |
| [`pc-clean`](pc-clean/SKILL.md) | Inspect hidden home files and folders and report cautious cleanup candidates without making changes |
| [`refactor`](refactor/SKILL.md) | Surgical, behavior-preserving code refactors: extract, rename, decompose, tighten types, apply patterns |
| [`research`](research/SKILL.md) | Hand a question to a background agent that reads primary sources and writes cited findings into the repo |
| [`teach`](teach/SKILL.md) | Teach a topic across sessions with structured learning records and practice |

## Install

A skill is a directory of plain Markdown, so installing one is a copy.

```bash
git clone https://github.com/elxecutor/skills.git
cp -r skills/refactor ~/.agents/skills/
```

Some setups scan `~/.config/opencode/skills/` instead of `~/.agents/skills/`. Check
which path yours reads, then copy the skills you want.

Most skills need only their Markdown and bundled references. Some include helper
scripts or rely on local tools and authentication; each skill documents its setup.
Never distribute local credentials (for example, Kaggle API tokens or Claude
session cookies). The `claude` and `kaggle` credential files are intentionally
excluded from this repository.

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
