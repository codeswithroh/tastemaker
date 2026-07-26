# Positioning: free core vs. paid variants

Decided 2026-07-26, resolving [#51](https://github.com/codeswithroh/tastemaker/issues/51).

## The decision

**The generative engine stays free and MIT.** Everything that makes tastemaker actually work — the palette generator and contrast contract, the macrostructure + component catalog + diversification engine, the narrative-arc discipline, the 50-gate anti-slop checklist, and the verbs (`study`, `audit`) — is the free core. This is not a crippled trial; it's the whole product a solo developer needs to stop shipping generic AI output.

**Specialized aesthetic variants are the paid differentiator.** Brutalist, minimalist, soft/premium-calm, and similar modes become a "tastemaker pro" pack, sold once (Gumroad/Lemon Squeezy), not bundled free.

## Why this way and not taste-skill's breadth-for-scale play

taste-skill gives away a whole family of specialized variants for free because their core skill is dial-tuned, not generative — `brutalist-skill` has to be its own file because nothing in their system *derives* brutalist from first principles. Breadth of free variants is genuinely their main lever for installs and sponsorship visibility, because there's no other axis of value to hold back.

tastemaker isn't built that way. The core engine already generates aesthetic variety (five moods → a fresh, contrast-verified palette every run, not a fixed swatch) and structural variety (macrostructures + component catalog + diversification, enforced so two builds don't repeat) from one system, not a pile of separately-authored variant files. That means:

- The free core is *already* differentiated and complete on its own — it doesn't need free variant breadth to be worth installing.
- A paid variant pack has something real to sell: not "five more markdown files copy-pasting the same rules with different adjectives" (taste-skill's actual structural weakness — a contrast bug fixed in one variant and forgotten in five others), but a **thin override layer on the shared engine** (see the architecture recommendation on #51: `references/modes/*.md`, each overriding specific dials — accent aggressiveness, radius, motion energy, density — against the one underlying system). That's a genuinely better engineering shape than taste-skill's flat duplication, and it's what makes the paid pack a real product instead of gatekeeping content that should've been free.

## What this means for #50 (multi-skill repo restructure)

**No restructure needed, and not for the reason #50 originally considered.** The public multi-skill folder layout (`skills/<name>/SKILL.md` per variant, discoverable via `npx skills add`) exists to serve *free* variants through the same public installer. Since the aesthetic variants are paid, they don't ship through the public MIT repo's skill-installer path at all — they're a separate purchased artifact (however that pack gets distributed once built), not another folder in `skills/`. The public repo stays exactly the shape it is today: one free skill, `skills/tastemaker/`.

If that ever changes — a free variant gets added for a genuinely different reason (not scale-driving breadth, but something like a real compatibility need) — revisit the multi-skill layout question then, on its own merits, not as a side effect of this decision.

## What ships next

- The mode-override-layer shape is now the target architecture for whenever the paid pack gets built (not scoped in this issue — a build task for later, tracked separately if/when work starts on it).
- The one real gap identified against taste-skill during this analysis — image-only comps mode, no equivalent in tastemaker at all — isn't a duplication-risk question like the aesthetic variants; it's new territory on its own merits. Tracked as [#56](https://github.com/codeswithroh/tastemaker/issues/56).
