# Contributing to tastemaker

Thanks for being here. Tastemaker gets better every time someone improves the palette generator, fixes a rough edge, or makes the docs clearer. This guide keeps that easy.

## Ways to help

- **Report a bug.** Something in the workflow or a script behaved wrong. Open a bug report.
- **Improve the palette generator.** A new mood, a wider or better-tuned hue range for an existing mood, a new color-harmony rule, or a better font pairing. This is the highest value contribution and the easiest to review.
- **Improve a pattern.** Better layout guidance, a sharper anti-slop check, a clearer reference file.
- **Fix the docs.** Typos, confusing wording, missing steps. Small doc PRs are always welcome.
- **Improve a script.** The Python helpers in `scripts/` can always be made more robust.

If you are not sure where to start, look at issues labeled [`good first issue`](https://github.com/codeswithroh/tastemaker/labels/good%20first%20issue).

## How the repo is laid out

- `SKILL.md` is the workflow the agent follows. Read it first.
- `references/` holds the deep material: mood ranges and type pairings, layout patterns, motion rules, asset sourcing, and checklists.
- `scripts/` holds small Python helpers (palette generation, color extraction, contrast checking, asset fetching, recoloring).
- `assets/` holds the GSAP motion starter and a dependency free fallback.
- `site/` is the marketing site and live demo.

Most contributions touch `references/` (guidance) or `scripts/` (tools).

## Local setup

```bash
git clone https://github.com/codeswithroh/tastemaker
cd tastemaker
pip install Pillow          # only needed for extract_palette.py
```

There is no build step. The scripts run directly:

```bash
python3 scripts/check_contrast.py --palette text=050315 bg=fbfbfe primary=2f27ce secondary=dedcff accent=433bff
python3 scripts/validate_assets.py .github/assets/
```

## Improving the palette generator

Color is not a fixed list of options anymore. `scripts/generate_palette.py` generates a fresh palette per project: a base hue within the target mood's range, a color-harmony rule for the accent, and each role's lightness solved against the contrast contract. This is the most common contribution surface now, and it splits into a few concrete shapes:

**Adding a new mood.** Open `scripts/generate_palette.py` and add an entry to the `MOODS` dict: a hue range (or a few disjoint ranges), a chroma range, and a default light/dark mode. Then add the mood to the keyword table in `references/style-tokens.md` (Step A) so the skill can classify an app idea into it, and a font pairing to the type-pairing table in Step B. Run the generator a dozen times with different seeds and look at the output, both as hex and rendered (paste into `realtimecolors.com` or a quick HTML swatch) before opening the PR.

**Adding or tuning a color-harmony rule.** Open the `HARMONIES` dict in `scripts/generate_palette.py`. Each entry is a function from a base hue to the accent and secondary hues it implies. Keep it a pure hue transform; the lightness solving is handled separately and should not need to change.

**Tuning an existing mood's range.** If a mood's generated palettes are drifting somewhere that does not feel like the mood (too muted, too saturated, hues that do not read as intended), narrow or shift its `hues`/`chroma` ranges in `MOODS`. This is a judgment call, so include a few example generated palettes (hex values, or a screenshot) in the PR description showing before and after.

**Whatever you change, verify the contract still holds.** Run the stress check before opening the PR:

```bash
python3 - <<'PY'
import subprocess, sys, re
sys.path.insert(0, 'scripts')
from check_contrast import ratio
for mood in ["premium","warm","technical","playful","elegant"]:
    for seed in range(30):
        out = subprocess.run(["python3","scripts/generate_palette.py","--mood",mood,"--seed",str(seed)],
                             capture_output=True, text=True).stdout
        roles = dict(re.findall(r"\s+([\w-]+)\s+#([0-9a-f]{6})", out))
        assert ratio(roles["text"], roles["bg"]) >= 4.5, (mood, seed, "text/bg")
        assert ratio(roles["on-primary"], roles["primary"]) >= 4.5, (mood, seed, "on-primary/primary")
        assert ratio(roles["primary"], roles["bg"]) >= 3.0, (mood, seed, "primary/bg")
        assert ratio(roles["accent"], roles["bg"]) >= 3.0, (mood, seed, "accent/bg")
print("OK: contract holds across moods and seeds")
PY
```

Do not ship a change that makes this fail. A palette that sometimes fails its own contract is worse than the fixed color scheme it replaced.

## Guidelines

- **Keep the copy simple.** Short sentences. Plain words. No em-dashes. The docs are read by people mid task, so clarity beats cleverness.
- **Verify, do not assume.** If you change a palette, run the contrast script. If you add or edit an SVG, run `validate_assets.py`. Numbers over vibes.
- **Follow the skill's own rules.** Visual over text, motion by default, real marks not letters in boxes. If a change would make the skill violate its own anti-slop checklist, rethink it.
- **One change per pull request.** Small, focused PRs get reviewed and merged faster.

## Pull request process

1. Fork the repo and create a branch: `git checkout -b my-change`.
2. Make your change. Run the relevant script to verify it.
3. Commit with a clear message that says what changed and why.
4. Open a pull request. Fill in the template. Link any related issue.
5. A maintainer will review. Small tweaks may be requested. That is normal.

## Reporting security issues

Please do not open a public issue for a security problem. See [SECURITY.md](SECURITY.md).

## Code of conduct

This project follows a [Code of Conduct](CODE_OF_CONDUCT.md). By taking part, you agree to uphold it.
