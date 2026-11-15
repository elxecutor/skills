# LESSON-FORMAT.md Format

HTML lessons are optional support, not the skill's primary artefact. The learner's own work is primary. Create a page only at the learner's request or when it directly enables an action that the agreed source and a short prompt cannot. Never replace the source with a parallel HTML course. These requirements apply only after that decision; they are not a session checklist.

When useful, use one self-contained HTML file in `lessons/`, named `0001-dash-case-name.html`, incrementing.

**This file is subject-agnostic.** It specifies what a lesson must *contain in principle*, not a fixed exercise format. A mathematics lesson, a guitar lesson, and a research-writing lesson should not look alike. If every lesson ends with the same quiz widget, the format has overridden the pedagogy.

Use the simplest accessible presentation that serves the task. Do not spend practice time polishing a page.

## Required elements

Every lesson needs at least:

1. **Objective** — what the learner will be able to *do* afterwards, in their terms. Not "understand X". If the objective cannot be observed, it cannot be verified, and unverifiable objectives quietly turn into self-report.
2. **Explanation** — concise, at their level, with the reasoning, not just the steps. Analogy, diagram, demonstration, derivation — whichever fits the discipline.
3. **A worked demonstration** — with the reasoning behind the non-obvious decisions visible, including dead ends considered.
4. **A participation point** — something the learner must decide, predict, construct, or perform. See below. This is not optional.
5. **An independent attempt** — a task with no step-by-step guidance and no answer in front of them.

> **Elements 4 and 5 are events, not page features.** Both must have *happened* — you must hold the learner's actual response and their actual output — before this lesson counts as taught, and before any state may be recorded from it. **Authoring the page is not delivering it.** A beautiful lesson nobody has done anything with supports no state.

Where the demonstration is auditory or visual — music, pronunciation, technique, anything where *hearing or seeing it* is the instruction — embed the audio or video (or link a local file) **and carry the same information in prose and notation**. A learner whose player failed, who is offline, or who cannot use that channel must not lose the demonstration. If the medium cannot be delivered in the file, move the demonstration into the conversation and say so.
6. **Feedback** — specific and actionable, ideally immediate and automatic where it can be correct.
7. **The follow-up activity** — what to practise, and when.

Include only what the lesson needs. Reference documents, a primary source to read, and links to related lessons belong here when they help; a prerequisite check only when this lesson genuinely rests on something shaky.

Also remind the learner you are their teacher: anything unclear, ask, at any stage.

## The participation point

**A lesson in which the learner only consumes has failed, however good the page looks.**

Somewhere in it, the learner does one of:

- Predict an outcome before it is revealed
- Choose between alternatives and justify the choice
- Produce something from a partial prompt rather than a complete one
- Explain *why*, not *what*
- Find the error in an example
- Perform the technique or manoeuvre themselves
- Interpret a result and say what it means

Where that lives depends on the discipline. Do not force the same mechanic onto every subject.

## Discipline-appropriate shapes

| Discipline | Typical participation | Typical independent attempt |
| --- | --- | --- |
| Mathematics | Predict before calculating; justify a method choice | An unfamiliar problem: pick a method, solve it, check it |
| Programming | Predict what code does before running it; find the bug | Write, test, and debug their own implementation |
| Engineering / circuits | Predict a measurement before simulating; explain a fault | Choose components, predict, measure, diagnose, modify |
| Simulation / software | Choose parameters; predict output; explain a discrepancy | Investigate a result that does not match expectation |
| Music | Play back what was just shown; predict how it sounds | Perform in a new context, at tempo, unaided |
| Language | Produce the target structure without a prompt; interpret meaning | Hold an unscripted exchange on an unfamiliar topic |
| Research / writing | Critique an argument; identify a weak source | Build and defend an original claim |
| Design | Justify a design decision; respond to critique | Produce original work with defended decisions |
| Hands-on / physical | Feel and describe the movement; self-correct | Perform in a changed situation, adapting to a new constraint |
| Anything else | Research what practitioners in that field actually decide and do; make that the participation | The task a competent practitioner in that field does unaided |

## Handing over material

Complete worked material — finished code, a full solution, a complete diagram, a ready-made layout — is a **demonstration, never a task**.

It is legitimate for showing a contract, an algorithm, or a failure mode. But the moment the learner can transcribe and run it, they have copied something, not learned it, and you must not record that as progress.

When the goal is for them to build something, leave a hole they must fill **with the answer not visible**: a function body, a derivation step, a component choice, a reward, a stopping condition, an error to fix.

## Interactive elements earn their place

Quizzes, simulations, diagrams, visualisations, code editors, and animations are tools, not decoration. Add one only when it makes something comprehensible or testable that would not be otherwise. A prettier page that measures nothing is a worse lesson.

Interactive assessment must check *meaningful* understanding whenever technically possible. **If a response cannot be reliably graded — open-ended explanation, design reasoning, why an approach failed, anything musical or physical — mark it `teacher-assessed` and assess it yourself in conversation.** Do not fabricate a score or hide a heuristic behind a green tick.

Any judgement must cite what the learner actually produced. If continuity needs a note, one sentence in `PROGRESS.md` is enough; formal states and a separate assessment record are not required. If there is no evidence, do not claim learning.

Keep quiz answer options the same length, ideally the same number of words, so formatting never leaks the answer.

## A lesson you did not teach from is not a lesson

If the explanation lives in the page, the verification belongs there too. Splitting explanation into HTML and questions into chat produces the worst of both: the learner reads the page, then answers you by paraphrasing it, and both of you call that learning.

Either teach it in the page and let its independent check stand, or teach it in conversation and do not also write a page.

## Assets

Reuse existing assets when useful. Do not build shared stylesheets, widgets, or a component system merely to support a single optional page. A self-contained page is fine; create supporting assets only when they directly serve the learner's task.

## Accessibility and validation

Semantic HTML, one `<h1>`, ordered headings, `<html lang>`, labelled inputs, `alt` text on meaningful images, visible focus, keyboard-operable interactive elements. Contrast that passes WCAG AA; layouts that survive 360 px width and print. Every interactive element needs a non-interactive fallback — never gate understanding behind a drag handle or a hover. Math has prose. Diagrams get a caption carrying the meaning. Never encode information in colour alone. Respect `prefers-reduced-motion`.

Before declaring a lesson done:

- Every relative link and asset path resolves. Nothing essential depends on a CDN or network.
- Scripts run without console errors; exercise logic actually grades what it claims to grade.
- Grading is correct on correct answers *and* on wrong ones — try both.
- **The independent attempt would actually fail for someone who did not learn it.** An assessment everything passes is decoration.
- Any item marked `teacher-assessed` really is.
- **You have received the learner's actual participation response and their actual independent output.** For physical, musical, and performance skills these happen *off-page*, in the learner's room — a widget they clicked is not participation, and a lesson file with no response attached has not been taught.

## Mathematics with MathJax

Render equations with **MathJax**, never ASCII approximations (`m * g * d`). Vendor the self-contained SVG bundle at `assets/mathjax/tex-svg.js` — copy it from an existing teach workspace, or fetch `https://cdn.jsdelivr.net/npm/mathjax@4/tex-svg.js`. It needs no network and works offline over `file://`.

```html
<script>
  window.MathJax = {
    tex: {
      inlineMath: [['$', '$'], ['\\(', '\\)']],
      displayMath: [['$$', '$$'], ['\\[', '\\]']]
    },
    svg: { fontCache: 'local' },
    a11y: { speech: false }
  };
</script>
<script src="../assets/mathjax/tex-svg.js"></script>
```

Keep `a11y: { speech: false }` — it stops MathJax lazy-loading its screen-reader component, the only piece not bundled, which would otherwise hit a CDN. Always keep readable prose next to the math; the TeX is a rendering aid and must never be the only copy.
