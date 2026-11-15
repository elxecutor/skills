# TEACHING-STRATEGY.md Format

**Optional, on demand.** Use this only when researched method choices need durable detail beyond the teaching contract. It is not a prerequisite to practice, a curriculum, or a mandatory session read. Follow the agreed source and learner-directed loop in `SKILL.md`.

`TEACHING-STRATEGY.md` lives in the workspace. It is the researched answer to *how should this subject be taught for this learner* — the bridge between what educational evidence says works and what you do next session.

It exists so teaching decisions are made against evidence rather than habit, and so a new session does not restart the thinking. It is a working strategy, **not a literature review**. Keep it short enough to reread every session; push detail into `RESOURCES.md`.

## Template

```md
# Teaching Strategy: {Topic}

**Learner:** {one line — level, prior background, mission fit}
**Confidence:** Provisional | Evidence-informed | Well-established
**Last reviewed:** {YYYY-MM-DD}

## What kind of learning this is
{2-4 sentences. Conceptual knowledge, procedural skill, physical performance, creative
production, or a mix — and roughly what fraction each. This decides the method more than
anything else: declarative facts and physical technique need very different practice shapes.}

## Evidence we are drawing on

| Method | Evidence | Population / conditions | Fits this learner? | Limitation |
| --- | --- | --- | --- | --- |
| {Method} | {citation + type, see RESOURCES.md} | {who it was measured on} | {yes / partly / no} | {what it does not cover} |

{Only methods you are actually going to use. Three to six rows is plenty. If evidence is
thin, say so here rather than padding the table.}

## What competent performance looks like here
{The authentic task in this discipline that a competent practitioner could do unaided — the
thing you are ultimately aiming at. Not a topic list. "Chooses a method for an unfamiliar
problem and justifies it", not "knows integration techniques". Name what they will *do* with
it. See the discipline table in [ASSESSMENT-FORMAT.md](./ASSESSMENT-FORMAT.md).}

## Moving from guided to independent
{How responsibility transfers in *this* discipline. Where the demonstration ends, what the
learner decides next, and what stops counting as evidence. For a physical skill this may be
"play from the diagram" → "play from memory" → "play it in a new key". For programming,
"fill the function body" → "write the function" → "design the data structure". For research,
"identify the weak source" → "evaluate it yourself" → "defend the judgement".}

## Chosen approach
{What you will actually do, and why this evidence supports it for this domain and learner.}

{State the guidance level per objective — Demonstration, Guided participation, Supported
application, or Independent — and what evidence will justify moving up a level. Do not plan
the whole course at one level; the level is per-objective and revisable.}

## Common misconceptions to pre-empt
- {Misconception} — {how it shows up when the learner holds it, and the correction}
- {…}

## Prerequisites
{Ordered list, marking the ones you must verify rather than assume.}

## How we will know it is working
{Observable behaviours that count as learning in this domain — see
[ASSESSMENT-FORMAT.md](./ASSESSMENT-FORMAT.md). Not a syllabus.}

## Practice and review design
{Retrieval style, spacing cadence for this domain, how interleaving applies, whether
in-session repetition matters more than across-session spacing.}

## Open questions
{Unresolved, contested, or unverified. What result would change the approach.}

## Revision triggers
{When to redo this: repeated failure, objective shift, new evidence, mission change.
Dates where a review is already due.}
```

## Rules

- **Evidence before preference.** If a method appears under *Chosen approach*, justify it from the table or label it a judgement call. Methods with no defensible basis go under *Open questions*, not into the plan.
- **It may start as a stub.** On day one, fill in *What kind of learning this is*, *Chosen approach*, and *Common misconceptions*. Fill the evidence table in as you verify sources. Do not stall a beginner's first lesson to complete ten sections of scaffolding.
- **Record the population.** Evidence from undergraduates is not evidence from a motivated adult with three hours a week. If the populations differ, say how you are adapting and why you are still using it.
- **Name uncertainty honestly.** *Provisional* means you are running an informed experiment on this learner, and their results are the next evidence. Say so out loud to them too.
- **Handle disagreement explicitly.** Record that sources conflict, which you followed, and the reasoning. Never split the difference or imply a consensus that does not exist.
- **No fabricated citations.** Every row traces to something in `RESOURCES.md`. If you could not open the source, mark it *unverified — model knowledge*. A plausible invented reference will be trusted later and will corrupt every downstream decision.
- **Be a working document.** Update it when reality diverges. A strategy recording only the original plan is worse than none, because it looks current.
- **Keep it to a screen or two.** If it has become a literature review, the conclusions belong in the table and the rest belongs in `RESOURCES.md`.

## When research is unavailable

If web access is missing:

1. Reuse what `RESOURCES.md` already holds — it is the curated fallback.
2. Rely on well-established general principles of learning science (retrieval, spacing, interleaving, worked examples, feedback), and **label them as established general findings rather than subject-specific evidence.**
3. Draw on model knowledge for subject structure and misconceptions, marking it unverified where you could not check it.
4. Set confidence to *Provisional*, name it as a limitation to the user, and teach.
5. Put a revision trigger on the strategy so it gets revisited when tools are available.

Never stall the learner waiting for research, and never pretend research happened.
