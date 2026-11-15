# GLOSSARY.md Format

`GLOSSARY.md` is the canonical language for this teaching workspace. All explainers, exercises, and learning records should adhere to its terminology. Building it is itself part of learning: compressing a concept into a tight definition is evidence the user understands it.

## Structure

```md
# {Topic} Glossary

{One or two sentence description of the topic this glossary covers.}

## Terms

**Hypertrophy**:
Muscle growth driven by mechanical tension and metabolic stress over repeated training sessions.
_Avoid_: Bulking, getting big

**Progressive overload**:
Systematically increasing the demand on a muscle over time — via load, volume, or intensity.
_Avoid_: Pushing harder, levelling up

**RPE (Rate of Perceived Exertion)**:
A 1–10 self-rating of how hard a set felt, where 10 is failure and 8 means two reps left in the tank.
_Avoid_: Effort score, intensity rating
```

## When to admit a term

The guard below tells you when *not* to add something. This is the trigger that tells you when to.

**When a concept reaches Comprehension or above in `PROGRESS.md`, and the user used the term themselves rather than echoing it back to you, admit it to the glossary in the same session.**

Do not wait for a ceremony, a review cycle, or the end of the topic. A term demonstrated in the lesson you just taught belongs in the glossary by the time the lesson closes — otherwise the glossary stays empty while the workspace fills with mastered concepts, which is the failure mode this rule exists to prevent. An empty glossary after a session that demonstrated real understanding is a signal you forgot, not a signal the user is not ready.

Admission is cheap: a one-line definition in the user's own framing. Keeping the vocabulary out of the glossary is not caution — it is the glossary failing at its job.

## The admission rule

**A term is admitted only when the user has demonstrated understanding of the concept it names.**

The glossary is a record of compressed knowledge, not a dictionary the user reads to learn from. It is a claim — "you own this word now" — so it should never be made on weaker evidence than understanding.

Sufficient evidence for admission:

- They compressed it themselves into a definition that is correct and non-trivial.
- They used it correctly, unprompted, in an explanation or a problem.
- They applied it correctly to a case they had not seen it in before.

Not sufficient:

- It appeared in a lesson.
- They can repeat your definition back to you.
- They got it right with the definition open next to them.
- It seems important for the topic.

That last set is the usual case, and it is why glossaries in learning workspaces drift into being unread word lists. If you are unsure, leave the term out and put the concept in `PROGRESS.md` at *Guided performance* instead. It costs nothing; a wrong admission corrupates every later lesson that assumes the vocabulary is settled.

To be fair, some terms have no second life outside the topic — a framework's internal vocabulary, a standard's defined modes. If a term must be used before it is understood, keep it in the lesson or reference doc where it was introduced, and admit it later when it sticks.

## Rules

- **Be opinionated.** When several words exist for the same concept, pick the best one and list the rest as aliases to avoid. This is how language compresses.
- **Keep definitions tight.** One or two sentences. Define what the term IS, not what it does or how to do it.
- **Use the glossary's own terms inside definitions.** Once a term is in the glossary, prefer it everywhere — including inside other definitions. This is what makes complex terms easier to grasp later.
- **Group under subheadings** when natural clusters emerge (e.g. `## Anatomy`, `## Programming`). A flat list is fine when terms cohere.
- **Flag ambiguities explicitly.** If a term is used loosely in the wider field, note the resolution: "In this workspace, 'set' always means a working set — warm-ups are tracked separately."
- **Revise as understanding deepens.** A definition the user wrote in week one may be wrong by week six. Update in place; do not leave stale entries.
- **Correct in place, do not delete.** When the user's model of a term was wrong and is now fixed, update the definition and note the correction. The wrong version is diagnostic signal for related concepts.