# MISSION.md Format

`MISSION.md` is optional. Usually the purpose line in the teaching contract is enough; do not create a second file to duplicate it. If a more detailed mission is useful, this document captures the _reason_ the user is learning. It guides priorities, not a parallel curriculum: the agreed source and learner's choices still govern sequence.

## Template

```md
# Mission: {Topic}

## Why
{1-3 sentences. The concrete real-world goal the user is chasing. What changes in their life
or work when they have this skill? Avoid abstract framings like "to understand X" — push for
the underlying outcome.}

## Success looks like
- {A specific, observable thing the user will be able to do, unaided}
- {Another specific thing}
- {…}

## Constraints
- {Time, budget, prior commitments, learning preferences, anything that bounds the approach}

## Out of scope
- {Adjacent topics the user explicitly does not want to chase right now — protects the zone of
  proximal development}
```

## Success means independent competence

"Success looks like" is not a list of topics covered. Each entry should be something the user can **do without you**, in a real situation, and that you could honestly observe.

Weak: "Understands Ohm's law."
Strong: "Sets up a divider in the lab, measures it, and explains why the reading is what it is."

Weak: "Has learned the major scales."
Strong: "Plays a G major scale to 100bpm with a metronome, clean, three sessions running."

Weak: "Understands Python data structures."
Strong: "Reaches for the right structure when a problem calls for it, without looking it up."

If an entry cannot be observed, it cannot be verified, and unverifiable success criteria quietly turn into self-report — which is exactly the failure mode this workspace exists to avoid.

When you can, note which level of independence each entry needs. Not every mission item needs full independence on day one; knowing that a stage performance needs to be *fluent under pressure* while a hobby bass session only needs *comfortable* changes what "done" means.

## Rules

- **One mission per workspace.** If the user wants to learn two unrelated things, that is two workspaces.
- **Concrete over abstract.** "Run a half marathon by October" beats "get fitter." "Ship a Rust CLI to my team" beats "learn Rust."
- **Push back on vagueness.** If the user cannot articulate why, interview them before writing anything. A bad mission is worse than no mission.
- **A compass, not a curriculum.** The mission decides priorities, depth, projects, prerequisites, and what can be postponed. It does not enumerate the lessons. Do not let it harden into a syllabus, and do not treat it as one when deciding what to teach next.
- **Revise when reality shifts.** Missions change. When the user's goal moves, update this file — don't leave a stale mission steering future sessions. **Confirm the change with the user** before it takes effect, then write a learning record so the change and its reason survive.
- **Keep it short.** If `MISSION.md` runs past a screen, it has stopped being a compass and started being a plan.
