# Contributing to tastemaker

Thanks for being here. Tastemaker gets better every time someone adds a preset, fixes a rough edge, or makes the docs clearer. This guide keeps that easy.

## Ways to help

- **Report a bug.** Something in the workflow or a script behaved wrong. Open a bug report.
- **Add a preset.** A new mood, palette, or font pairing. This is the highest value contribution and the easiest to review.
- **Improve a pattern.** Better layout guidance, a sharper anti-slop check, a clearer reference file.
- **Fix the docs.** Typos, confusing wording, missing steps. Small doc PRs are always welcome.
- **Improve a script.** The Python helpers in `scripts/` can always be made more robust.

If you are not sure where to start, look at issues labeled [`good first issue`](https://github.com/codeswithroh/tastemaker/labels/good%20first%20issue).

## How the repo is laid out

- `SKILL.md` is the workflow the agent follows. Read it first.
- `references/` holds the deep material: presets, layout patterns, motion rules, asset sourcing, and checklists.
- `scripts/` holds small Python helpers (color extraction, contrast checking, asset fetching, recoloring).
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

## Adding a new preset

This is the most common contribution, so here is the exact path:

1. Open `references/style-tokens.md` and add your preset under the mood list, following the shape of the existing five.
2. Pick a palette (five roles: text, background, primary, secondary, accent) and a Google Font pairing.
3. Verify it with the contrast script. Both checks must pass:
   ```bash
   python3 scripts/check_contrast.py --palette text=<hex> bg=<hex> primary=<hex> secondary=<hex> accent=<hex>
   ```
   Body text vs background and white label vs primary both need to clear 4.5:1. If a color fails, adjust it and run again. Do not ship a preset that fails.
4. Add a short note on which app ideas the mood fits, so the skill can match it.
5. If you add a dark mode companion, run the same check against the dark background.

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
