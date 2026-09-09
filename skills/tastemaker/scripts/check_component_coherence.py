#!/usr/bin/env python3
"""Static scan for the "stitched together from six registries" tell.

references/component-sourcing.md's "director's actual job" section states
six coherence rules (one icon family, one radius/shadow/spacing scale, one
motion engine) but until now nothing checked them mechanically — they were
self-reported the same way structural rotation and copy specificity used to
be before scripts/check_structure_history.py and check_copy_diversity.py.
This is that check for pulled-component coherence: it doesn't verify taste,
it verifies that the *symptoms* of an uncoherent restyle pass (mixed icon
families, two motion engines, an unbounded spread of raw shadow/radius
literals instead of the locked scale) aren't present.
"""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

EXTENSIONS = {".css", ".html", ".js", ".jsx", ".mjs", ".ts", ".tsx", ".vue", ".svelte"}
SKIP_DIRS = {".git", ".next", ".netlify", ".playwright-cli", "node_modules", "dist", "build", "coverage"}

# icon package -> regex matching an import/usage of it
ICON_PACKAGES = {
    "lucide-react": r"from\s+[\"']lucide-react[\"']|lucide-react/icons",
    "lucide (vanilla)": r"from\s+[\"']lucide[\"']",
    "@tabler/icons-react": r"from\s+[\"']@tabler/icons-react[\"']",
    "phosphor-react / @phosphor-icons": r"from\s+[\"']phosphor-react[\"']|from\s+[\"']@phosphor-icons/",
    "heroicons": r"from\s+[\"']@heroicons/",
    "react-icons": r"from\s+[\"']react-icons/",
    "@radix-ui/react-icons": r"from\s+[\"']@radix-ui/react-icons[\"']",
    "iconify (iconify-icon element)": r"<iconify-icon\b",
    "remixicon": r"from\s+[\"']@remixicon/|ri-[a-z-]+-line|ri-[a-z-]+-fill",
    "feather icons": r"from\s+[\"']feather-icons(?:-react)?[\"']",
}

MOTION_ENGINES = {
    "GSAP": r"from\s+[\"']gsap[\"']|gsap\.(?:to|from|fromTo|timeline)\(",
    "Motion / Framer Motion": r"from\s+[\"'](?:framer-motion|motion|motion/react)[\"']",
    "anime.js": r"from\s+[\"']animejs[\"']|anime\(\{",
}

RAW_BOX_SHADOW_RE = re.compile(r"box-shadow\s*:\s*([^;\n}]+)", re.IGNORECASE)
RAW_RADIUS_RE = re.compile(r"border-radius\s*:\s*(-?\d+(?:\.\d+)?(?:px|rem|em))\b", re.IGNORECASE)
CSS_VAR_TOKEN_RE = re.compile(r"var\(--", re.IGNORECASE)

RAW_SHADOW_DISTINCT_THRESHOLD = 4
RAW_RADIUS_DISTINCT_THRESHOLD = 5


@dataclass
class Finding:
    severity: str
    rule: str
    message: str


def iter_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_file() and path.suffix in EXTENSIONS:
            files.append(path)
            continue
        if not path.is_dir():
            continue
        for child in path.rglob("*"):
            if any(part in SKIP_DIRS for part in child.parts):
                continue
            if child.is_file() and child.suffix in EXTENSIONS:
                files.append(child)
    return sorted(set(files))


def scan_icon_families(files: list[Path]) -> list[Finding]:
    hits: dict[str, set[Path]] = defaultdict(set)
    for path in files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for name, pattern in ICON_PACKAGES.items():
            if re.search(pattern, text):
                hits[name].add(path)
    if len(hits) <= 1:
        return []
    lines = [f"{name} (in {len(paths)} file(s), e.g. {sorted(paths)[0]})" for name, paths in hits.items()]
    return [
        Finding(
            "HIGH",
            "mixed-icon-families",
            "Multiple icon packages detected in the same project: " + "; ".join(lines) + ". "
            "Pulled components often each bring their own default (lucide via shadcn, "
            "something else via a different registry) — pick one family and convert the rest.",
        )
    ]


def scan_motion_engines(files: list[Path]) -> list[Finding]:
    hits: dict[str, set[Path]] = defaultdict(set)
    for path in files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for name, pattern in MOTION_ENGINES.items():
            if re.search(pattern, text):
                hits[name].add(path)
    if len(hits) <= 1:
        return []
    lines = [f"{name} (in {len(paths)} file(s), e.g. {sorted(paths)[0]})" for name, paths in hits.items()]
    return [
        Finding(
            "HIGH",
            "mixed-motion-engines",
            "Multiple motion engines detected: " + "; ".join(lines) + ". "
            "references/animation-guidelines.md and component-sourcing.md are explicit: one engine per "
            "project unless a pulled component forces a second — if that's genuinely why, say so; "
            "otherwise standardize on one.",
        )
    ]


def scan_raw_scale_values(files: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    distinct_shadows: dict[str, set[Path]] = defaultdict(set)
    distinct_radii: dict[str, set[Path]] = defaultdict(set)

    for path in files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in RAW_BOX_SHADOW_RE.finditer(text):
            value = match.group(1).strip()
            if CSS_VAR_TOKEN_RE.search(value) or value.lower() == "none":
                continue
            distinct_shadows[value].add(path)
        for match in RAW_RADIUS_RE.finditer(text):
            distinct_radii[match.group(1)].add(path)

    if len(distinct_shadows) >= RAW_SHADOW_DISTINCT_THRESHOLD:
        findings.append(
            Finding(
                "MEDIUM",
                "shadow-scale-drift",
                f"{len(distinct_shadows)} distinct hard-coded box-shadow values found across "
                f"{len(files)} scanned file(s), none referencing a CSS custom property. This is "
                "the signature of components pulled from different registries each keeping their "
                "own shadow depth. Consolidate into the lock's shadow scale as tokens.",
            )
        )
    if len(distinct_radii) >= RAW_RADIUS_DISTINCT_THRESHOLD:
        findings.append(
            Finding(
                "MEDIUM",
                "radius-scale-drift",
                f"{len(distinct_radii)} distinct hard-coded border-radius values found "
                f"({', '.join(sorted(distinct_radii)[:8])}{'…' if len(distinct_radii) > 8 else ''}), "
                "none referencing a CSS custom property. Reduce to the lock's radius scale.",
            )
        )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scan for signs of un-restyled, stitched-together pulled components."
    )
    parser.add_argument("paths", nargs="+", type=Path, help="Files or directories to scan")
    parser.add_argument("--fail-on", choices=("high", "medium", "none"), default="high")
    args = parser.parse_args()

    files = iter_files(args.paths)
    if not files:
        print("No matching source files found.")
        return 0

    findings: list[Finding] = []
    findings.extend(scan_icon_families(files))
    findings.extend(scan_motion_engines(files))
    findings.extend(scan_raw_scale_values(files))

    if not findings:
        print(f"Component coherence check passed: scanned {len(files)} files, one icon family / one motion engine / scale tokens in use.")
        return 0

    order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    findings.sort(key=lambda f: (order.get(f.severity, 9), f.rule))
    for finding in findings:
        print(f"{finding.severity} [{finding.rule}] {finding.message}")

    if args.fail_on == "none":
        return 0
    if args.fail_on == "medium":
        return 1
    return 1 if any(f.severity == "HIGH" for f in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
