---
name: claude
description: Full access to the user's Claude.ai via the claude-cli tool — list, read, create, rename, delete, and discuss. Holds a progressive back-and-forth via a subagent until a conclusion is reached. Use when the user says @claude, mentions Claude conversations, or wants anything done on Claude web.
---

# Claude via claude-cli

Route every Claude.ai interaction through `~/.local/bin/claude-cli` via bash.
Cookie auto-loads from `~/.config/opencode/claude-cookie`.
Never invent conversation content — only report what the tool returns.

## Commands

- List conversations: `~/.local/bin/claude-cli --list`
- Show history: `~/.local/bin/claude-cli --history -c <conversation-uuid>`
- Send message: `~/.local/bin/claude-cli -c <conversation-uuid> "message"`
- New conversation: `~/.local/bin/claude-cli --new "title"` (title optional)
- Rename: `~/.local/bin/claude-cli --rename -c <conversation-uuid> "new name"`
- Delete: `~/.local/bin/claude-cli --delete -c <conversation-uuid>`

## Routing

- `list` / `list conversations` → run `--list`, present each UUID with its name.
- UUID only → run `--history` for that UUID, then summarize it.
- UUID + message → run `--history` first to load context, then send the message with `-c`, return the output.
- Message with no UUID → run `--list` first so a conversation can be picked; ask the user which one if ambiguous.
- `new chat` / `new conversation` (+ optional title and opening message) → run
  `--new "title"`, then start the subagent loop below on the fresh UUID. If an
  opening message was given, send it as the first turn.
- `rename` → run `--rename -c <uuid> "new name"`, confirm the new name.
- `delete` → only on explicit user request; echo the conversation name from
  `--list` first so the target is unambiguous, then run `--delete -c <uuid>`.

## Progressive conversation (subagent loop)

For anything beyond list/history — any question, problem, or review — do not
chat inline. Spawn ONE subagent via the task tool (`subagent_type: general`)
and let it carry the back-and-forth to a conclusion:

1. Resolve the conversation UUID — given, picked from `--list`, or freshly created
   with `--new` for a new chat (ask if ambiguous) — run `--history` to load
   context, and build the opening message with workspace context folded in
   (see below).
2. Instruct the subagent to loop on that same UUID: send via
   `~/.local/bin/claude-cli -c <uuid> "message"` (multi-line and quotes are
   safe — the CLI JSON-encodes the body), then immediately verify with
   `~/.local/bin/claude-cli --history -c <uuid>`: the new human message AND a
   fresh assistant reply must appear in the tail before the next turn. If the
   send printed an error or history shows nothing new, stop and surface the
   error instead of looping blindly — then either conclude or follow up, never
   stop mid-thread with a partial answer.
3. Each follow-up must progress the thread: answer Claude's questions from the
   workspace, challenge gaps, demand specifics. No repeated or stalled questions.
4. Conclude when Claude gives a definitive answer with no open questions, when a
   blocker appears (auth failure → report `claude-cli --update-cookie`), or at a
   turn cap of 8. The subagent returns the conclusion plus a condensed transcript.

## Context

The subagent has full workspace access. Every message it sends — opening and
follow-ups — folds in whatever is under discussion: the current topic plus the
relevant file snippets or diffs (condensed, not whole dumps). Keep each message
focused so Claude gets what it needs without noise.

## Auth failure

If output says cookie expired/missing, stop and tell the user to run
`claude-cli --update-cookie`.
