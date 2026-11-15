# RESOURCES.md Format

`RESOURCES.md` is an optional curated source set. The agreed primary source remains the source of truth; this list supplements rather than replaces it. Create it only when useful sources need to persist beyond the compact source map. No resource catalogue, methodology bibliography, or community list is required before practice. Check facts against trusted sources, not parametric guesses, whether or not a catalogue exists.

Three kinds of source, three different jobs:

| Group | What it is | What it is for |
| --- | --- | --- |
| **Subject knowledge** | Texts, docs, papers, courses that explain *the content* | Explaining and demonstrating correctly |
| **Teaching methodology** | Research on *how to teach this* | Choosing methods in `TEACHING-STRATEGY.md` |
| **Wisdom** | Experienced practitioners and communities | How the work is actually done, and what the pitfalls are |

Keep them distinct. A textbook is evidence about content, not evidence about pedagogy — and citing it as the latter is a category error that quietly wrecks a teaching strategy.

## Structure

```md
# {Topic} Resources

## Subject knowledge

- [Book: _The Science and Practice of Strength Training_ — Zatsiorsky & Kraemer](https://example.com)
  Foundational text on strength training and adaptation. Use for: anything to do with periodisation,
  recovery, intensity zones.

## Teaching methodology

- [Meta-analysis of worked-example instruction — {Author et al.}, {Journal}, {year}](https://example.com)
  Type: meta-analysis. Finding: worked examples outperformed unsupported problem solving for
  novices, effect diminished with prior knowledge. Population: undergraduate engineering
  coursework. Limitation: lab and procedural skills not represented. Informs: we sequence
  worked example → completion problem → independent problem for the first two months.
  Verified: 2026-03-02.

- {Thing we believe but have not verified}
  Type: model knowledge. Informs: default approach only. **Unverified — do not cite to the
  learner as evidence.**

## Wisdom (Communities)

- [r/weightroom](https://reddit.com/r/weightroom)
  High-signal subreddit, moderated against bro-science. Use for: programme critique, plateau
  troubleshooting.

- Local: Tuesday strength class at {gym name}
  Use for: real-time coaching feedback on lifts.
```

## Teaching-methodology entries

For anything cited in `TEACHING-STRATEGY.md`, record all six:

1. **Title and link.**
2. **Type** — meta-analysis, systematic review, RCT, quasi-experimental, correlational, practitioner report, opinion piece. The type is what tells the reader how much to trust it.
3. **Main finding** — the actual result, in one line, with an effect size if there was one.
4. **Population and conditions** — who it was measured on, under what conditions, for how long.
5. **Limitations or uncertainty** — what it does not cover, and where findings conflict.
6. **How it informs instruction** — what we will actually do differently because of it.

A teaching-methodology entry without #6 is a reading list, not a teaching tool.

## Rules

- **High-trust only.** Prefer primary sources, recognised experts, peer-reviewed work, and communities with strong moderation. If a resource is marketing dressed as education, leave it out.
- **Never fabricate.** Do not invent a paper, author, journal, year, finding, or consensus. If you could not open it, either leave it out or mark it *unverified — model knowledge*. A plausible fake citation is worse than none: it will be trusted in a later session and will quietly corrupt a teaching decision. This is the single most important rule in this file.
- **Annotate every entry.** A bare link is useless in three months. Add one line on what it covers and when to reach for it.
- **Prefer the synthesis over the primary study** when one exists. Read the review, then follow its citation only if you need to check its scope.
- **Population is not a detail.** Evidence from undergraduates, from children, or from a different domain does not transfer automatically. Record it so a later session does not over-read the finding.
- **Surface gaps explicitly.** If no good resource exists for an area the mission needs, write a `## Gaps` section listing what is missing. This drives future search.
- **Prune ruthlessly.** A resource that turned out to be wrong, shallow, or off-mission should be removed, not buried. Better five sharp sources than thirty mediocre ones.
- **Do not build a database.** This file is for sources you will *use*. A bibliography nobody consults is not a curriculum.
- **Record community preferences.** If the user has opted out of joining communities, note it here so future sessions stop proposing them.
