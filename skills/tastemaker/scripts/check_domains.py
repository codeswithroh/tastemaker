#!/usr/bin/env python3
"""Fail the build if the skill references any domain that is not explicitly vetted.

This exists because a security audit found a flagged phishing domain
(`logoyoyo.com`) recommended inside this skill's own documentation. Removing it
once is not a fix — the fix is that it, or anything like it, cannot come back
without someone deliberately editing the allowlist in this file.

What it does:
  * walks every text file in the skill (and optionally the whole repo),
  * extracts every http(s) URL and bare domain reference,
  * fails on anything in DENY (known-bad, permanently banned),
  * fails on anything not in the vetted allowlist.

Usage:
    python3 scripts/check_domains.py                # scan the skill
    python3 scripts/check_domains.py <path> [...]   # scan specific paths

Exit code 0 = clean, 1 = unvetted or banned domain found.
"""

from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _netguard import ALLOWED_HOSTS  # noqa: E402

# Permanently banned. Removed after a security audit flagged it as a phishing
# risk with an unverifiable license. Never reintroduce.
DENY = {
    "logoyoyo.com": "flagged as a phishing risk by security scanners; license was never verifiable",
}

# Domains the skill is allowed to *mention* in docs or fetch from. The network
# allowlist (ALLOWED_HOSTS in _netguard.py) is folded in automatically, so the
# runtime guard and this static check can never drift apart.
DOC_ALLOWED = {
    # source hosting / the project itself
    "github.com", "raw.githubusercontent.com", "githubusercontent.com",
    "codeswithroh.github.io", "tastemaker-skill.online", "tastemaker-skill.pages.dev",
    "skills.sh", "www.skills.sh",
    # asset + font sources documented in the skill
    "undraw.co", "openverse.org", "iconify.design", "pixabay.com",
    "fonts.googleapis.com", "fonts.gstatic.com", "streamlinehq.com",
    # component registries (references/component-sourcing.md)
    "ui.shadcn.com", "registry.watermelon.sh", "kokonutui.com", "ui.bklit.com",
    "21st.dev", "motion.dev", "npmjs.com", "unpkg.com",
    # tooling / standards referenced in docs
    "developer.mozilla.org", "www.w3.org", "w3.org", "wcag.com",
    "gsap.com", "greensock.com", "vercel.com", "linear.app",
    "buy.polar.sh", "polar.sh", "fazier.com", "producthunt.com",
    "creativecommons.org", "opensource.org", "choosealicense.com",
    "schema.org", "developers.cloudflare.com",
    # design references cited in the docs (studied, linked, or named as
    # anti-references — all reachable, reputable, none fetched automatically)
    "coolors.co", "fontpair.co", "realtimecolors.com", "make.design",
    "motionsites.ai", "grayblocks.net", "symbolfyi.com", "www.typotheque.com",
    "typotheque.com", "framer.com", "webflow.com",
}

ALLOWED = DOC_ALLOWED | set(ALLOWED_HOSTS)

URL_RE = re.compile(r"https?://([A-Za-z0-9.\-]+)")
# Bare domain mentions in prose, e.g. "logoyoyo.com is a library of…"
BARE_RE = re.compile(
    r"\b((?:[a-z0-9](?:[a-z0-9\-]*[a-z0-9])?\.)+"
    r"(?:com|net|org|io|dev|ai|sh|co|app|design|co\.uk))\b"
)

SKIP_DIRS = {".git", "node_modules", "dist", ".wrangler", "__pycache__", "out", ".venv"}
# The guard files themselves necessarily contain both the banned domain (as a
# DENY entry) and lookalike test strings. Scanning them would be self-defeating.
SELF = {"check_domains.py", "_netguard.py", "test_security.py"}
TEXT_EXT = {
    ".md", ".py", ".js", ".jsx", ".ts", ".tsx", ".html", ".css",
    ".json", ".yml", ".yaml", ".txt", ".toml", ".svg",
}


def is_allowed(host: str) -> bool:
    host = host.lower().strip(".")
    if host in ALLOWED:
        return True
    return any(host.endswith("." + a) for a in ALLOWED)


def banned_reason(host: str) -> str | None:
    host = host.lower().strip(".")
    for bad, why in DENY.items():
        if host == bad or host.endswith("." + bad):
            return why
    return None


def scan_file(path: str):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            lines = fh.readlines()
    except OSError:
        return
    for n, line in enumerate(lines, 1):
        hosts = set(URL_RE.findall(line)) | set(BARE_RE.findall(line))
        for host in hosts:
            why = banned_reason(host)
            if why:
                yield n, host, f"BANNED — {why}", line.strip()[:110]
            elif not is_allowed(host):
                yield n, host, "not in the vetted allowlist", line.strip()[:110]


def walk(roots):
    for root in roots:
        if os.path.isfile(root):
            yield root
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fn in filenames:
                if fn in SELF:
                    continue
                if os.path.splitext(fn)[1].lower() in TEXT_EXT:
                    yield os.path.join(dirpath, fn)


def main() -> int:
    roots = sys.argv[1:] or [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]
    findings = []
    scanned = 0
    for path in walk(roots):
        scanned += 1
        for n, host, why, ctx in scan_file(path):
            findings.append((path, n, host, why, ctx))

    if not findings:
        print(f"Domain check passed: {scanned} files, 0 unvetted domains.")
        return 0

    banned = [f for f in findings if f[3].startswith("BANNED")]
    for path, n, host, why, ctx in findings:
        rel = os.path.relpath(path)
        print(f"{'BANNED' if why.startswith('BANNED') else 'UNVETTED'} {rel}:{n}  {host}")
        print(f"    {why}")
        print(f"    {ctx}")
    print(
        f"\n{len(findings)} finding(s) across {scanned} files "
        f"({len(banned)} banned).\n"
        "If a domain is legitimate, add it to DOC_ALLOWED in this file "
        "(or ALLOWED_HOSTS in _netguard.py if the skill fetches from it) "
        "with a real reason. Never add anything in DENY."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
