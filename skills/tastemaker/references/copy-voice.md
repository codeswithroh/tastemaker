# Copy voice — writing headlines that couldn't be anyone else's

## The problem this solves

`scripts/generate_palette.py` and `references/macrostructures.md` stop two projects from looking alike. Nothing stops them from *reading* alike. A page can pick a fresh palette, a rotated macrostructure, real photography, and still open with "The smart way to manage your workflow" — a sentence that is true of roughly four thousand SaaS products and specific to none of them. Copy is usually the fastest tell a reader hits (the headline is the first thing read, before any visual craft registers), and it's the one axis this skill didn't have a generator, a bank, or a memory file for until now.

`scripts/anti_slop_scan.py` catches individual banned *words* ("elevate," "seamless," "unleash"). That's necessary but not sufficient — swapping "elevate" for "transform" defeats the word list while writing the exact same sentence. The actual tell is the **sentence template**, not the vocabulary: "The [adjective] way to [verb]," "Built for [audience] who [verb]," "[Verb] your [noun] in [time]," "Where [noun] meets [noun]." These templates are what read as generated regardless of which synonym fills the slots. This file, plus `scripts/check_copy_diversity.py`, treats sentence shape as the thing to diversify — the same move `diversification.md` makes for page shape.

## Step 1 — Ground every headline in one concrete, checkable fact

Before writing a headline, subhead, or feature line, answer: **what is one fact about this specific product that would be false if you swapped in a close competitor's name?** If nothing survives that swap, the copy is a value-prop mad-lib, not real copy — no matter how well it's worded. The fact can be:

- A specific mechanism ("renders diffs before you merge," not "streamlines your workflow").
- A specific number, pulled from the actual brief (a real price, a real limit, a real speed) — never invented (same honesty rule as `macrostructures.md`'s Stat-Led section).
- A specific user action the product uniquely enables ("comment directly on the running chart," not "collaborate seamlessly").
- A specific point of contrast with the obvious alternative ("no build step," "runs on your own infra," "one file, not a config folder").

Write the headline as the sharpest sentence containing that fact, not as a decorated version of "this product is good." `references/hero-guidelines.md`'s "five-second answer" template (*This product helps [user] achieve [outcome] by [mechanism]*) is the right starting scaffold — the mechanism slot is where the concrete fact goes; don't let it collapse into a generic outcome word ("efficiency," "growth," "success") with no mechanism attached.

## Step 2 — Write three candidates from different angles, pick by elimination

Per `references/prototype-variants.md`'s logic applied to copy: write three headline candidates that differ in **angle**, not just phrasing, before picking one:

1. **Mechanism-led** — leads with what the product specifically does.
2. **Outcome-led** — leads with the change in the user's situation, still grounded in the Step 1 fact.
3. **Tension-led** — leads with the specific problem or contrast the product resolves.

Reject any candidate that matches a pattern in the template bank below. Pick the survivor that reads best for the mood and macrostructure already locked — don't default to whichever came out first.

## Voice dials by mood

Copy voice is a real axis, same status as palette and type — it should shift with the project's locked mood (`references/style-tokens.md`), not default to one register everywhere. These are dials, not scripts to fill in.

| Mood | Sentence rhythm | Formality | What to avoid |
|---|---|---|---|
| **Premium / confident** | Short, declarative, few subordinate clauses. Confidence from certainty, not adjectives. | Address as "you," but restrained — no exclamation points. | Stacking intensifiers ("incredibly powerful, truly seamless"). One strong claim beats three inflated ones. |
| **Warm / approachable** | Slightly longer, more conversational; contractions allowed. | Friendly, first names welcome in examples. | Baby-talk simplicity that undersells competence, or forced cheerfulness ("Yay! Let's get started!"). |
| **Technical / builder-facing** | Terse, information-dense, comfortable with real technical nouns (the actual protocol/format/primitive, not a vague abstraction of it). | Peer-to-peer, no marketing gloss. | Explaining the obvious to the audience it's for; hype adjectives ("blazing fast," "next-gen") in place of a real number. |
| **Playful / consumer social** | Punchy, can break grammar rules for rhythm, more verbs than nouns. | Casual, can address the reader directly and informally. | Forced internet-speak that isn't the brand's actual voice; emoji standing in for icons (already a scanner HIGH finding). |
| **Elegant / editorial** | Measured, longer sentences allowed, more comfortable with a subordinate clause or an em-dash. | Understated, closer to a magazine lede than an ad. | Overwrought adjectives reaching for luxury ("exquisite," "unparalleled," "curated" used as filler) — restraint reads more premium than the adjective does. |

State which mood's dial you're writing to before drafting, the same way Step 2 states the palette mood — it's one line, and it's what keeps the three candidates in Step 2 from defaulting to the same flat register regardless of the project.

## The template bank — sentence shapes to reject on sight

These are shapes, not words — a candidate matching one of these patterns is generic by construction even if every individual word is fine. Reject and rewrite rather than reaching for a synonym.

- **"The [adjective] way to [verb]."** ("The smart way to invoice," "The modern way to collaborate.")
- **"Built for [audience] who [verb]."** as a headline (fine as a targeting subhead if it also carries the Step 1 fact — the failure is using it as the *whole* claim).
- **"[Verb] your [noun] in [time]."** ("Ship your product in minutes," "Launch your store in seconds.") — unless the time claim is real and specific to a measured workflow, not a round marketing number.
- **"Where [noun] meets [noun]."**
- **"[Adjective], [adjective] [noun]."** as a headline — a comma-spliced adjective pair standing in for an actual claim ("Simple, powerful analytics.")
- **"Everything you need to [verb]."**
- **"[Noun] made [adjective]."** ("Invoicing made easy," "Design made simple.")
- **"Say goodbye to [problem]."**
- **"Your [noun], reimagined/reinvented."**
- **"One platform for all your [noun]."**

`scripts/anti_slop_scan.py` runs a subset of these as regex (see its `AI_COPY_PHRASES` and template patterns) as a mechanical floor. Treat the full list here as the thing to check by eye — regex catches the exact shapes, a human/model read catches the near-misses regex can't parameterize.

## Cross-project memory — the same problem structure has, solved the same way

A page can avoid every template above and still repeat itself project to project if the *same specific headline* (or a near-paraphrase) keeps winning the Step 2 elimination — the model has favorite sentences the same way it has a favorite macrostructure. `~/.tastemaker/copy-history.json` tracks recent shipped headlines and CTA labels across every project, mirroring `~/.tastemaker/structure-history.json` in `references/diversification.md`.

```json
[
  { "id": "tracejam-2026-08-01", "date": "2026-08-01", "project": "tracejam", "surface": "hero", "headline": "See the query before it runs.", "cta": "Watch a trace", "angle": "mechanism", "outcome": "kept" },
  { "id": "meridian-studio-2026-07-23", "date": "2026-07-23", "project": "meridian-studio", "surface": "hero", "headline": "Twelve rooms. One idea each.", "cta": "See the work", "angle": "tension", "outcome": "pending" }
]
```

- **Append an entry in the same pass** as the CSS stamp and the structure-history entries (Step 4 of `SKILL.md`) — one write covers structure and copy together. Record which of Step 2's three candidate angles (`mechanism`/`outcome`/`tension`) won, and set `outcome` to `"pending"` — it isn't known yet.
- **Trim to the last ~40 entries.**
- **Run `scripts/check_copy_diversity.py --headline "<text>" --cta "<text>"` before finalizing the hero** (Step 4, alongside `check_structure_history.py`). It flags: (a) a match against the template bank, (b) high word-overlap against a recent global headline (near-paraphrase), (c) a banned/generic phrase from the expanded list. Non-fatal — same nudge posture as the structure check — but state the result in the pre-emit self-critique's Specificity score.
- **Update `outcome` at Step 5**, matching by `id`, the same close-the-loop step `references/diversification.md` runs for structure. Once enough entries resolve, `scripts/summarize_outcomes.py` reports kept-vs-rejected rates per angle alongside the structure rates — if `tension`-led headlines are getting kept more than `mechanism`-led ones across projects, that's real signal for which of the three Step 2 candidates to favor when more than one reads fine. Same caveats as the structure version: tie-break only, never an excuse to skip writing three real candidates, and small samples (under 4 resolved) are noise.

## Reuse rules

- Product name, real feature names, and real numbers are never subject to the template check — those are exactly the specific content the check exists to protect room for.
- A user-supplied headline (the brief hands you exact copy) is never overridden by this file — ground the *rest* of the page's copy to match its register instead.
- CTA labels get the same specificity bar as headlines at smaller scale: "Get started" and "Learn more" are legal defaults only when nothing more specific fits ("Watch a trace," "See the work," "Start your first deploy" beat generic verbs when the product supports a named first action).
