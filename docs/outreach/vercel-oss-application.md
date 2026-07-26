# Vercel Open Source Program — application draft

Drafted 2026-07-26, resolving part of [#52](https://github.com/codeswithroh/tastemaker/issues/52). **Not submitted** — sending is a manual step for the repo owner.

## Status check (verified, not assumed)

As of this writing, Vercel's OSS Program page states **applications are currently closed and will reopen in August** — days away from today. No live application form was found; Vercel directs pre-application questions to their community forum at `community.vercel.com/c/open-source/45`. Re-check `vercel.com/open-source-program` when reopened for the actual submission form.

## A real eligibility gap to resolve before applying

Vercel's stated eligibility includes: **"hosted on or intended to host on Vercel."** The tastemaker marketing site (`site/`) is currently deployed on **Netlify**, not Vercel (`site/.netlify/netlify.toml`). This needs a decision before applying:

- **Migrate the site to Vercel** — genuinely low-cost: it's a static HTML/CSS/GSAP-from-CDN site with no build step, and both platforms have near-identical static-hosting DX. If applying, this is honestly the cleaner path — "hosted on Vercel" beats "intend to."
- **Apply under "intended to host on Vercel"** and migrate only if/when accepted — riskier, since it's a stated claim about a future action, not current fact.

**This repo does not migrate hosting unilaterally — that's a real, user-facing infrastructure change (DNS, deploy pipeline) requiring explicit confirmation, not something to do as part of drafting outreach materials.** Decide this before submitting.

## Draft application content

**Project name:** tastemaker

**One-line description:** A Claude Code skill that grounds AI-generated UI in real reference images, a generated-and-contrast-verified palette, and a persistent per-developer taste profile — instead of the generic AI-slop defaults every model reaches for.

**Repo:** https://github.com/codeswithroh/tastemaker (MIT licensed)

**Current stats (honest, as of 2026-07-26 — an early-stage project, stated as such, not inflated):** 58 stars, 6 forks. Created 2026-07-09 — under three weeks old. This is not yet a large-scale project; the application should be framed on technical depth and active maintenance velocity, not current install/star volume.

**Why tastemaker fits the program, beyond raw numbers:**

- **Real technical depth, not prompt-tuning.** The core isn't a static rules file — it's a generative engine: `scripts/generate_palette.py` produces a fresh, WCAG-contrast-verified palette per project (never a fixed swatch), `scripts/check_contrast.py` enforces a real color contract (not just body-text contrast — every fill/border/state pairing a build introduces), and a macrostructure + component-catalog + diversification system enforces genuine structural variety build to build (nav/footer/hero archetypes must differ from the last build, tracked in a project-memory file). This is a real dev-tool with measurable, checkable output, not a skill that produces plausible-sounding text.
- **Active, disciplined maintenance.** A `research/` directory (tracked in [#54](https://github.com/codeswithroh/tastemaker/issues/54)) documents the actual empirical investigation behind several of the skill's rules (real DOM measurement, structural studies of comparable tools, contrast-failure analysis) — the kind of rigor a technical evaluator can verify directly, not take on faith. Reference it in the actual submission once it ships.
- **A real Code of Conduct already in place** (`CODE_OF_CONDUCT.md`), satisfying that eligibility line directly.
- **Credits would go directly to project infrastructure** — site hosting (pending the migration decision above), and any future tooling (e.g. testing the skill's generated output against real deploy environments) — squarely inside the program's "use credits for the project itself" requirement.

**What we'd ask for:** the standard $3,600 in platform credits over 12 months plus the OSS Starter Pack, per the program's published benefits — no custom ask beyond the standard package, since this is an early-stage project without the scale to justify more.
