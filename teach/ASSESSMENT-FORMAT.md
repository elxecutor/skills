# ASSESSMENT-FORMAT.md

**Optional formal reference.** Use these labels only when requested or genuinely useful. Routine tutoring verifies through learner work and needs no state table, separate quiz, or assessment report. This file does not override the contract, learner-requested skips, or minimal-state rules in `SKILL.md`.

Assessment in this workspace answers one question: **can the learner do this thing without you?**

It is not coverage, not a progress bar, and not a certificate. A lesson that was read is not evidence. A guided task that succeeded *is* evidence — of guided performance, which is a lower rung than it usually gets credited for.

This file is **subject-agnostic**. What counts as an artefact differs by discipline; what counts as *theirs* does not.

## The seven states

States, not scores. They are evidence categories, **not a rigid sequence** — a physical skill may skip *Comprehension* entirely, and a theoretical topic may never need *Retention* on a given day.

| State | Observable evidence |
| --- | --- |
| **Exposure** | Encountered it. Carries no weight alone. |
| **Recognition** | Identifies or selects the correct thing among options or distractors. |
| **Comprehension** | Explains the principle and its reasoning accurately, in their own words. |
| **Guided performance** | Performs it with assistance: hints, scaffold, reference open, demonstration alongside. |
| **Independent performance** | Performs an appropriate task **without step-by-step guidance**. |
| **Transfer** | Applies it to a meaningfully different situation, or diagnoses a novel failure using it. |
| **Retention** | Still does it after a meaningful delay, unaided. |

### Recognition is not comprehension

This is the most common misclassification, and it is cheap to fall into because a recognition item is easy to write, easy to grade, and feels like a test.

- "Which of these is the Q-function?" → *Recognition*.
- "What does the Q-function mean and when would you use it?" → *Comprehension*.
- "Which chord is this?" → *Recognition*. "Play it, then find a chord sharing two notes but not its function." → *Independent performance*.
- "Which of these four topologies meets the spec?" → *Recognition*. "Choose a topology for a new spec." → *Independent performance*.

If the learner can pick the right answer but cannot produce it unprompted, they are at *Recognition*. Record it as such. A learner who can only recognise is far from incompetent — they have a real foundation — but building further on *Recognition* produces a learner who scores well and cannot act.

The same collapse happens everywhere: naming a chord is not playing it; identifying a fallacy in someone else's argument is not constructing a sound one; picking the correct circuit topology from four diagrams is not designing one.

## Gradual release of responsibility

Guidance level is a per-objective decision, not a default. Too little too early strands the learner; too much too long makes them dependent and manufactures the appearance of competence.

| Level | Who is doing the thinking | Looks like |
| --- | --- | --- |
| **Demonstration** | Tutor | You model it and narrate the reasoning, including the decisions and the wrong paths avoided. |
| **Guided participation** | Shared | They contribute to a problem you are structuring; you supply the frame and catch errors. |
| **Supported application** | Learner | They make the decisions; you give targeted hints only when stuck. |
| **Independent performance** | Learner | An appropriate task with no step-by-step guidance from you. |
| **Transfer and reinforcement** | Learner | A different context, revisited over time. |

Two rules govern it:

- **Release on demonstrated competence**, not on elapsed lessons or on your optimism. If they are performing at a level unaided, stop scaffolding — support that never fades becomes dependency, and it also hides whether they can actually do it.
- **Do not rush.** A learner who has never had the concept demonstrated is not ready for independent work. Being stuck is not evidence that the method is wrong; check whether the support level was the problem before changing anything else.

Support must also **fade within a session**, not just across sessions: worked example → completion task → hinted task → independent task.

## Setting criteria

Before teaching anything substantial, write down what the relevant states look like concretely. What counts as independent performance is discipline-specific — see the table below.

## Authentic evidence by discipline

Do not assume quizzes, code, or written explanation are universally the best demonstration. Pick the evidence a competent instructor in that field would actually accept.

| Discipline | What independent performance looks like | What is only *guided* or lower |
| --- | --- | --- |
| **Mathematics** | Chooses an appropriate method for an unfamiliar problem, justifies why, checks the answer | Substituting into a supplied formula; reproducing a worked calculation |
| **Programming** | Designs logic, writes it, debugs, tests, builds a solution | Typing code from a lesson; running a program you supplied and reporting the output |
| **Circuit / electrical engineering** | Selects components, predicts behaviour, interprets measurements, diagnoses a fault, modifies a design | Clicking through a simulation tutorial; building a circuit from a step-by-step procedure |
| **Music** | Performs it, in time, with control; applies it in a new musical context; recognises it by ear | Naming chords; reproducing fingerings from a diagram; explaining theory |
| **Language** | Communicates meaning in an unscripted exchange; produces the target structures spontaneously | Repeating phrases; completing a fill-in-the-blank from a pattern |
| **Research / academic writing** | Evaluates sources, constructs and defends an argument, revises in response to critique | Summarising an analysis you read; outlining someone else's argument |
| **Simulation / technical software** | Understands model assumptions, chooses parameters, predicts behaviour, investigates discrepancies | Following the software's step-by-step instructions to a result |
| **Design / creative** | Produces original work, makes and defends design decisions, revises in response to critique | Reproducing a layout or style you specified |
| **Hands-on / physical** | Performs the task in a new situation, with control, adapting to a changed condition | Following a demonstration step by step; holding the posture as shown |
| **Anything else** | The task a competent practitioner in that field performs unaided — research it and write it here explicitly | Following that field's own tutorials, manuals, or walkthroughs step by step |

## The authorship test

**Before recording any state above Guided performance, name the specific thing the learner produced that they did not receive from you.**

Not a description of their answer. The artefact itself: code they wrote, a performance they played, an argument they built, a layout they designed, an error they found, a configuration they chose.

- If the learner typed code out of a lesson and ran it, that artefact is **not theirs**. It is yours, transcribed.
- If they reproduced a worked calculation, filled in your template, played your fingering diagram, or followed your procedure, that artefact is not theirs either — in any discipline.
- If they chose from options you supplied, that is selection, not production. Not an artefact.

**A freely composed explanation, argument, diagnosis, or design rationale *is* an artefact.** This rule is not about suppressing talk — it is about suppressing selection and transcription. Asking someone to explain is how *Comprehension* is assessed in any subject whose competence is verbal: mathematics, language, research, design, law, medicine. The bar is that they **composed** it, unprompted and unexplained, about a case you had not already solved in front of them.

Ask yourself the blunt version: **if the learner had done nothing at all, would this evidence still exist?** If yes, it proves nothing about them.

This test is the last thing you do before writing to `PROGRESS.md`, not a reflection. It exists because the failure it catches is invisible from the inside — the session feels productive, the outputs look right, and nothing signals that the learner produced nothing at all.

## Following an instruction is not the same as deciding

> **Ask what the learner chooses, not what they were told to do.** "Change the goal to position 3" and they change it is compliance — they executed an instruction you specified. "Make one change to this environment and say what you expect it to do" is a decision. The first is at most *Guided performance*, however cleanly it runs.

The same applies outside technical work. Being handed the vocabulary for a concept and then deploying it correctly on the case you supplied shows they can *use* the term, not that they can *think* with it.

If a task can be completed by transcribing your last instruction, it does not count as evidence of independence.

## Never mistake completion for mastery

None of these establish independent competence on their own. They may contribute to learning; they are not evidence of it:

- Reading or finishing an HTML lesson
- Watching a tutorial or demonstration through
- Copying a solution, or typing provided code
- Reproducing a worked example, calculation, diagram, or layout
- Repeating demonstrated steps or a provided procedure
- Running a program, simulation, or instrument you set up
- Answering a recognition question
- Saying "Done"
- Executing an AI-generated solution successfully

When one of these happens, record what was *actually* demonstrated — usually *Exposure* or *Guided performance* — and move on to the independent version. Never inflate it because the artefact looked finished.

## The proportionate rule

**A completed action can be the evidence, when the action is the skill.** If the objective was "send an authenticated request with `curl`" and they did it unaided and showed the output, that may be the whole state. Do not follow it with a written quiz about HTTP verbs — that tests something adjacent and unrelated.

Do not force an examination after a trivial action. Conversely, when the objective is *understanding*, a performed action is not enough: they must also explain, predict, or choose.

## Guided vs independent

The most common false positive is promoting guided success to independent competence.

- A guided success tells you the teaching is landing and the level is roughly right.
- It says nothing about whether they can do it alone.
- The next step is usually **one** unscaffolded attempt, not a fresh battery of checks.

Conversely, do not re-teach from scratch because an independent attempt failed on a technicality — that is a fluency or attention failure, not evidence the concept is absent.

## When you cannot observe the performance

Some skills cannot be verified from a conversation: playing an instrument, soldering, free-diving, physical technique, or anything requiring equipment or a room.

**Judge by the channel you actually have.** A written exchange *is* direct observation of written production — word choice, register, reasoning, structure. For a language learner that is real, gradeable evidence for the written sub-skill, not a report. What is *not* observable in text is pronunciation, intonation, prosody, and listening comprehension: ask for a recording, or mark those `unverified beyond report`. Never assess how something sounded from a romanisation or a spelling.

**Say so. Do not claim mastery you have not observed.**

- Ask for evidence that can substitute: a recording, a photo, a measurement, a timestamped log, a video, or the learner's own detailed account.
- If no such evidence exists, record the honest state: *Guided performance, unverified beyond report*.
- Label it `teacher-assessed` and write the evidence sentence as reported, not as observed — `reported as competent; not independently observed`.
- Offer to verify next session, and keep the concept in the review queue until it is.

A plausible-sounding claim that you verified something you never saw is the worst possible failure here: it corrupts the learner's sense of their own progress *and* the record that every future session depends on.

## Automated vs teacher-assessed

Grade automatically only what can be graded reliably: numeric answers, syntax, exact matches, simulated results the code computes.

Grade yourself, in conversation, when the answer is open: explanation, reasoning, design choices, diagnosis, writing quality, anything musical or physical.

**Label it `teacher-assessed` and actually assess it.** Never invent a score, never present a heuristic as a measurement. A misleading automated check is worse than no check, because the learner trusts it and you will later trust it too.

### The teacher-assessed artefact

Almost all genuine verification lands here — explanation, prediction, diagnosis, design reasoning, playing an instrument — so this is the load-bearing path, not an exception. It therefore needs an output, not just a label.

**A formal judgement must cite evidence, not merely assert a label.** If recording a state, include one sentence naming what the learner actually produced and the help given: their own words, their code, the recording, the measurement. Do not create an assessment record for every interaction.

If you cannot produce that sentence, the state is *Exposure*.

Feedback in conversation should point to the learner's actual work. Persist a short evidence sentence in `PROGRESS.md` only when it affects resuming; do not duplicate it across files. A lesson marked entirely `teacher-assessed`, with no actual evidence anywhere, has not been assessed — it has been labelled.

## Design rules

- **Verify with a case you have not already solved.** If the only example in play is the one you just walked through, you have nothing to test. Before asking, build a second, different case — a new situation, a change you did not announce, or a prediction the learner would get wrong if they were pattern-matching.
- **New numbers is not a different case.** Substituting fresh values into the structure you just demonstrated re-tests arithmetic, not method selection, and a good memoriser passes it every time. Above *Recognition*, the fresh case must change *what the learner has to decide*: a different method to choose, a different condition to diagnose, a different context to apply to.
- **If you catch yourself writing a question whose answer you gave one message earlier, throw it away.**
- **Test understanding, not wording.** Re-ask the lesson's own question with its own phrasing and you have measured recall of a page.
- **Prefer prediction and diagnosis.** "What happens if you halve this resistance?" and "This reading is wrong — why?" both demand a model of the thing. Recognition questions demand much less.
- **Change one thing at a time.** Vary the surface, hold the concept constant — so a failure is informative.
- **Use transfer tasks for anything expected to matter beyond the lesson.** Familiarity with one worked example is not understanding.
- **Interleave when discriminating matters.** Mixing related problem types forces the learner to first decide *which* method applies, which is where real expertise lives.
- **Make wrong answers informative.** A useful wrong option is one a learner with a specific misconception would choose.

## Reporting to the learner

Say what their work shows, what remains uncertain, and the next action. Use formal state names only if useful or requested. Keep it to a few sentences.

Be honest about weak states. "You can do this with the reference sheet open; try it without" is far more useful than vague encouragement, and it tells them exactly where they stand.
