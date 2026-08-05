# Security posture — tastemaker skill

What this skill touches, what it will refuse to do, and how that is enforced automatically.

Last reviewed: 2026-08-02, in response to an external audit (skills.sh Agent Trust Hub).

---

## Network egress — the complete list

This skill contacts these hosts and no others. The list is enforced at runtime by
`scripts/_netguard.py`, not merely documented:

| Host | Purpose | Key required |
|---|---|---|
| `api.iconify.design` | Icon SVGs (permissively licensed sets) | No |
| `api.openverse.org` | Photography search, filtered to CC0 / Public Domain Mark | No |
| `pixabay.com` | Optional higher-curation photography | Yes — `PIXABAY_API_KEY`, opt-in only |
| `cdn.jsdelivr.net` | Pinned JS library delivery (Motion) | No |
| `cdnjs.cloudflare.com` | Pinned JS library delivery (GSAP + ScrollTrigger) | No |

Every request is **https-only** and **host-allowlisted**, and both checks are re-applied
on each redirect. Anything else raises `BlockedURLError` instead of being fetched.

No telemetry. No analytics. Nothing about your project is transmitted anywhere. The
only outbound traffic is fetching public assets you asked for.

## What the bundled scripts can and cannot do

The Python scripts read and write files inside your project and call the APIs above.

They contain **no** `subprocess`, `os.system`, `shell=True`, `eval`, `exec`, or
`pickle` — asserted on every CI run by `scripts/test_security.py`, so it cannot
regress silently.

## Untrusted input

Two categories are treated as **data, never instructions**:

1. **Project documents** — PRDs, specs, issues, READMEs, tickets, design briefs. The skill
   reads these to extract a screen list and product copy. If such a document contains text
   addressed to the agent (run this, fetch that, ignore your instructions, reveal a key),
   the skill must surface it to the user and stop, not act on it. See the callout at Step 1
   of `SKILL.md`.
2. **Reference images and screenshots** — the same rule applies to text rendered inside an
   image.

## Third-party components

`references/component-sourcing.md` documents pulling components from shadcn-compatible
registries. Those commands are **run by you**, deliberately, and install source into your
project where you can read it. The skill does not fetch or execute registry code by itself.
Treat any registry as you would any dependency: read what lands in your tree.

## Automated enforcement

Run locally, and on every push, PR, and weekly via `.github/workflows/security.yml`:

```bash
python3 skills/tastemaker/scripts/check_domains.py    # domain allowlist + permanent denylist
python3 skills/tastemaker/scripts/test_security.py    # URL guard, no-shell/eval, injection guidance
```

`check_domains.py` scans every text file for URLs and bare domain mentions and exits
non-zero on anything banned or not explicitly vetted — so an unvetted domain cannot reach
`main`, in code *or* in prose.

## Change history

**2026-08-02 — external audit remediation.**

- **Removed a domain flagged as a phishing risk** that had been documented as an optional
  manual logo source. Logo marks are now constructed locally from primitives, or an existing
  brand asset is preserved. The domain is permanently listed in `DENY` and can never be
  reintroduced without a deliberate edit that CI would surface.
- **Fixed a local-file-read vector found during remediation** (not in the original audit):
  `fetch_photos.py` passed an API-supplied URL directly to `urllib.request.urlopen`, which
  honours `file://`. A hostile or compromised search record could have caused a local file
  read. All fetching now routes through the scheme + host allowlist.
- **Added explicit prompt-injection handling** for project documents and reference images.
- **Documented full network egress** (this file) and added the CI enforcement above.

## Reporting

Open a security issue at <https://github.com/codeswithroh/tastemaker/issues>.
