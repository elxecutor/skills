---
name: grilling
description: Stress-test a plan, decision, or idea through structured rounds of dependency-aware questions until its assumptions and trade-offs are explicit. Use when the user asks to be grilled, challenged, or helped to think through a choice.
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled — the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round using the `ask` tool (the `question` tool in this environment): include every frontier question in a single tool call and wait for the user's answers before the next round. Do not ask these questions only as plain chat text.

## Question-tool presentation

Use the fields of the `question` tool for their intended roles. The tool is already an interactive form; do not simulate one with Markdown, emoji, arrows, option lists, or a "Submit" question inside the prompt.

- `header`: a short, scannable title (30 characters or fewer), such as `Primary outcome`.
- `question`: a direct, self-contained decision question. Start with its round number in plain text, for example `Q1. What is the most important problem to solve at launch?` Add only the context needed to make the choice; use short plain-text paragraphs if needed.
- `options`: provide mutually distinct decisions. Keep each `label` short and action-oriented; put the implication or rationale in `description`.
- Put the recommended option **first** and label it `… (Recommended)`. State why it is recommended in that option's description, rather than as a separate pseudo-option or a line in the prompt.
- Use plain text in all tool fields. Avoid Markdown syntax (`**`, headings, lists), decorative symbols, and repeating the question in an option.
- Include an `Other` option only when a genuinely open-ended answer is useful. Do not add a separate confirm/submit question: the tool handles submission.

Example shape:

```text
header: "Primary outcome"
question: "Q1. What is the most important problem to solve at launch?"
options:
  - label: "Trusted campus trading (Recommended)"
    description: "Focuses the MVP on fast, safer exchanges among verified community members."
  - label: "Broad marketplace"
    description: "Launch with many categories and audiences from day one."
  - label: "Student income"
    description: "Prioritize services and tools that help students earn money."
```

Each round the user answers reshapes the tree — settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it — don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report — ask the rest of the frontier now. The _decisions_ are the user's — put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.
