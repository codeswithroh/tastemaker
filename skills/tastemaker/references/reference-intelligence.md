# Reference intelligence

Use this when a project starts with no supplied references, or when the brief asks for a modern, professional, current-feeling direction without naming examples. The goal is to build from a real reference field instead of the model's default memory of "good UI."

## Design read

Before picking colors or writing code, state one line:

`Design read: <surface type> for <audience>, mode <Persuade|Operate|Read|Experience>, with <visual lane>, dials <variance>/<motion>/<density>/<art direction>.`

Modes:

- **Persuade:** landing pages, campaigns, pricing, portfolios where the visitor must decide and act.
- **Operate:** apps, dashboards, editors, admin tools, settings, workflows.
- **Read:** docs, articles, changelogs, help centers, explainers.
- **Experience:** galleries, showcases, immersive portfolios, demos where the artifact leads.

Default dials, then adjust from the brief:

| Dial | Default | Meaning |
|---|---:|---|
| Variance | 7 | 1 = symmetrical and conventional, 10 = asymmetric and art-directed |
| Motion | 5 | 1 = still, 10 = cinematic or physics-led |
| Density | 4 | 1 = gallery-airy, 10 = cockpit-dense |
| Art direction | 7 | 1 = safe commercial, 10 = strong point of view |

Adjust by surface:

- Persuade: variance 7-9, motion 5-8, density 3-5.
- Operate: variance 3-6, motion 2-5, density 6-9.
- Read: variance 4-6, motion 1-4, density 3-6.
- Experience: variance 8-10, motion 6-9, density set by the artifact.

The dials are not user-facing decoration. They decide layout asymmetry, amount of motion, section density, and how much visual risk the first viewport can carry.

## Build a reference board

Create `.tastemaker/reference-board.md` on cold starts and major redesigns.

Use five lanes:

1. **Direct competitors:** what this category already ships.
2. **Adjacent products:** tools or brands with a similar audience, but a different category.
3. **Cultural sources:** publications, physical objects, places, rituals, or graphics the audience already understands.
4. **Interface systems:** official design systems or product languages that fit the surface.
5. **Anti-references:** common category defaults this project should avoid.

**If a web search or web-fetch tool is available in this session, using it here is mandatory, not optional.** This is the actual point of failure in practice: the tools are available in most sessions, but "if web search or screenshot tools are available" reads as permission to skip them when writing an inferred board is faster, and an inferred board is what the model defaults to under time pressure — which quietly turns "grounded in real references" back into "grounded in the model's memory of good UI," the exact thing this file exists to prevent. Concretely, before writing the design read:

1. Run at least one real search for the product's category (e.g. "best \<category\> landing pages 2026", "\<category\> SaaS design", the names of 2-3 known players in the space if you know them).
2. Fetch or screenshot at least 2-3 of the resulting current, real sites — not sites recalled from training data, actually retrieved this session.
3. Pull concrete, current traits from what you actually saw: a real layout choice, a real type treatment, a real motion pattern — not a paraphrase of what that company's site probably still looks like.

Collect 5-9 concrete references across the five lanes this way, and write the source URLs, dates viewed, and the traits you are borrowing. **Only fall back to an inferred board when the tools are genuinely unavailable in this session** (check the tool list, don't guess) or a specific fetch fails after a real attempt — never as a shortcut past a step that takes a few tool calls. When falling back, label it `inferred, not viewed` and say plainly that search/fetch tools were unavailable or failed; do not pretend you saw sources, and do not let "inferred" quietly become the default path in a session where it didn't have to be.

Reference board format:

```markdown
# Reference board

Created: <date>
Mode: <Persuade|Operate|Read|Experience>
Design read: <one-line read>
Dials: variance <n>, motion <n>, density <n>, art direction <n>
Sourcing: <viewed via search/fetch on <date> | inferred, tools unavailable | inferred, fetch failed after attempt>

## Quality bar
- <source or inferred reference>: <what sets the craft bar>

## Borrow
- Palette/material: <source> -> <trait, not copied pixels>
- Type/hierarchy: <source> -> <trait>
- Layout/composition: <source> -> <trait>
- Motion/interaction: <source> -> <trait>
- Asset language: <source> -> <trait>

## Avoid
- <category rut or anti-reference>

## Direction contract
- Thesis: <what this surface proves>
- First viewport: <composition and primary visual>
- System: <tokens, structure, motion, assets>
- Risk: <what could go wrong if overdone>
```

## Pick the implementation foundation

Use official systems when the brief clearly lives inside one:

| Brief reads as | Reach for |
|---|---|
| Microsoft or enterprise productivity | Fluent UI |
| Google or Android-adjacent product | Material 3 |
| IBM or enterprise analytics | Carbon |
| Shopify admin surface | Polaris |
| GitHub/dev community | Primer |
| UK public service | GOV.UK Frontend |
| US public service | USWDS |
| Accessible custom React app | Radix primitives or shadcn/ui, adapted away from defaults |

One system per project. Check the repo's dependency files before importing anything. If the package is missing, either install it or use the existing stack and record the reason.

When the brief is an aesthetic rather than a system, build with the project's stack and state what is inspiration versus official design-system use. Glass, bento, editorial, brutalist, kinetic, and dark-tech directions are aesthetic lanes, not packages.

## Turn references into a direction

Do not copy a reference composition. Extract:

- A color/material strategy.
- A type and hierarchy strategy.
- A layout grammar.
- A motion grammar.
- An asset grammar.
- A list of tells to avoid.

Then write the direction contract into `.tastemaker/style-lock.md` and the build stamp. The contract should be recognizable even if all copy is removed.

## If no user references exist

You still need a quality bar. **Search current sources — this is the default path when tools allow it, not the option to skip.** Use the reference board lanes above. When search or fetch is genuinely not available this session, derive the board from the product's world and mark it as inferred. This keeps the work grounded without blocking the build — but grounded-via-search is the intended common case in a tool-enabled session, and inferred should be the exception you can point to a reason for, not the default outcome.

## Do not

- Do not ask the user for CSS values, color preferences, or font names unless the brand requires them.
- Do not default to a familiar category treatment just because the user gave no references.
- Do not treat a generated image or reference screenshot as a promise to copy. It is a quality bar and grammar source.
- Do not invent customer logos, metrics, quotes, or public proof while building a reference-led surface.
- Do not skip the search/fetch step because an inferred board is faster to write — if the tools are on the tool list this session, reaching for "inferred" without trying them first is the exact failure this file exists to close, not a neutral shortcut.
