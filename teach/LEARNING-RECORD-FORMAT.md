# Learning Record Format

Learning records are optional. Create `learning-records/` only when a durable, non-obvious decision cannot be preserved adequately in the compact contract or progress note. Use sequential numbering: `0001-slug.md`, `0002-slug.md`, etc. Never duplicate routine progress evidence here.

They are the teaching equivalent of ADRs: non-obvious lessons, key insights, and stated prior knowledge that steer future sessions. They are used to calculate the zone of proximal development.

They are **not** the live progress state — that is `PROGRESS.md`. Records are sparse and permanent; progress is current and gets rewritten.

## Template

```md
# {Short title of what was learned or established}

{1-3 sentences: what was learned (or what prior knowledge was established), and why it matters for future sessions.}
```

That is the whole format. A learning record can be a single paragraph. The value is recording _that_ this is now known and _why_ it changes what to teach next — not in filling out sections.

## Optional sections

Only include these when they add genuine value. Most records won't need them.

- **Status** frontmatter (`active | superseded by LR-NNNN`) — when an earlier understanding turns out to be wrong and is replaced.
- **Evidence** — how the user demonstrated it. A question answered, an exercise completed unaided, a circuit built and diagnosed, prior experience cited. Required in spirit for any claim of understanding, even when you keep it to a clause.
- **Implications** — what this unlocks or rules out for future sessions. Worth recording when non-obvious.

## Numbering

Scan `learning-records/` for the highest existing number and increment by one.

## When to write a learning record

Consider one only when the durable-record test above is met, for example:

1. **The user demonstrated genuine understanding or performance of something non-trivial** — an artefact they produced without being handed it, in any discipline: code they wrote, an argument they built, a performance they played, a design they made, a calculation they chose to do. Not just exposure, and not a procedure they followed. This sets a new floor for what to teach next. Name the evidence.
2. **The user disclosed prior knowledge** — "I already know X." Record it so future sessions don't re-teach it, and record the _depth_ claimed so the diagnostic can test it rather than re-ask.
3. **A misconception was corrected** — they previously believed something wrong and now see why. These are high-value: they predict future stumbling blocks for related topics. Write these in full, including what the wrong belief was; the wrong model is the diagnostic clue later.
4. **The mission shifted in response to learning** — they discovered they cared about something different than they thought. Cross-link to [MISSION.md](./MISSION-FORMAT.md) and update it.
5. **A teaching method failed and you changed it** — record what you tried, what happened, and what replaced it. This stops the next session from repeating a dead end, and it is the difference between a tutor and a loop.

### What does _not_ qualify

- Material that was merely covered. Coverage is not learning. Wait for evidence.
- Routine per-session state. That belongs in `PROGRESS.md`.
- Anything already captured tersely in [GLOSSARY.md](./GLOSSARY-FORMAT.md) as a term definition. Don't duplicate.
- Session-by-session activity logs. Learning records are not a journal — they are decision-grade insights.

## Evidence standard

A record asserting understanding without evidence is a guess wearing a suit. Write the evidence in the same sentence where you can: "Chose series resistors after predicting the current division, unaided" — not "Understands series and parallel circuits."

The evidence must be an artefact **the learner produced without being handed it**. Typing out your worked solution, filling in your template, or following your procedure is not their achievement, whatever it looks like. If the artefact came from you, the state is at most *Guided performance* — and often just *Exposure*.

Claimed knowledge is not demonstrated knowledge. If the user asserted a skill you have not tested, record it as *claimed, unverified* and say so. That phrasing is what stops a future session from building on something that turns out to be missing.

For practical skills you could not observe, say so in the record: "reports clean tempo; not independently observed." Do not write a clean state for something you never watched — it corrupts both the learner's sense of their progress and every future session that reads this file.

## Supersession

When a later record contradicts an earlier one (their understanding deepened, or turned out to be wrong), mark the old record `Status: superseded by LR-NNNN` rather than deleting it. The history of how understanding evolved is itself useful signal — and a superseded belief often predicts the misconception will return.
