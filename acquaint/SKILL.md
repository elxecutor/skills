---
name: acquaint
description: Read the workspace init files (AGENTS.md and its linked docs) to acquaint yourself with project conventions, collaboration guidelines, and system access rules. Use at the start of a new session or when the user says "acquaint yourself" or "read the init files".
---

# Acquaint

## Goal

Know what to do in the context of this project — not to summarize files, but to extract actionable guidance for how to behave, what workflows to follow, and what constraints apply.

## Steps

1. Locate AGENTS.md
   - Try `./AGENTS.md` (workspace root)
   - Try `~/.local/share/opencode/AGENTS.md` (opencode config)
   - If neither exists, ask the user for the path

2. Read AGENTS.md and extract relative links (e.g., `./docs/COLLABORATION.md`)
   - Resolve paths relative to the file's location
   - Skip broken links; note them for the user

3. Extract actionable knowledge:
   - **Behavioral expectations** — how should the agent act? (proactive vs reactive, when to ask, when to act)
   - **Workflows** — git branching, testing, linting, commit conventions, PR process
   - **Constraints** — what NOT to do (no sudo, no committing secrets, no unprompted commits)
   - **Environment** — venv paths, tool locations, system-specific rules
   - **Missing/broken files** — report any linked docs that couldn't be read

4. Internalize, don't recite
   - The output of this skill is the agent's understanding, not a report to the user
   - Only surface issues (broken links, ambiguities) that affect the ability to work
