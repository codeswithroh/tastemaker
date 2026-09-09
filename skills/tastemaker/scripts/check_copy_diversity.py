#!/usr/bin/env python3
"""Flag generic-template and cross-project-repeated headline/CTA copy.

anti_slop_scan.py catches individual banned *words* ("elevate", "seamless").
This script catches the sentence *shapes* that read as generated regardless
of which synonym fills the slots ("The smart way to X", "Built for Y who Z"),
plus near-duplicate headlines across projects via the same cross-project
memory pattern check_structure_history.py uses for page structure.

See references/copy-voice.md for the reasoning and the template bank this
mirrors.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

DEFAULT_GLOBAL_PATH = Path.home() / ".tastemaker" / "copy-history.json"

# Sentence *shapes*, not words — a match here is generic by construction.
TEMPLATE_PATTERNS = [
    (r"\bthe\s+\w+\s+way\s+to\s+\w+", "the-[adj]-way-to", '"The [adjective] way to [verb]"'),
    (r"\bbuilt\s+for\s+\w+(?:\s+\w+)?\s+who\s+\w+", "built-for-who", '"Built for [audience] who [verb]" as the whole claim'),
    (r"^\s*\w+\s+your\s+\w+\s+in\s+(?:seconds|minutes|hours|no\s+time)", "verb-your-noun-in-time", '"[Verb] your [noun] in [time]"'),
    (r"\bwhere\s+\w+\s+meets\s+\w+", "where-x-meets-y", '"Where [noun] meets [noun]"'),
    (r"^\s*\w+(?:,\s*\w+)+\s+\w+\s*[.!]?\s*$", "adj-adj-noun", '"[Adjective], [adjective] [noun]" as a headline'),
    (r"\beverything\s+you\s+need\s+to\s+\w+", "everything-you-need", '"Everything you need to [verb]"'),
    (r"^\s*\w+\s+made\s+\w+\s*[.!]?\s*$", "noun-made-adj", '"[Noun] made [adjective]"'),
    (r"\bsay\s+goodbye\s+to\b", "say-goodbye-to", '"Say goodbye to [problem]"'),
    (r"\byour\s+\w+,?\s+(?:reimagined|reinvented)\b", "noun-reimagined", '"Your [noun], reimagined/reinvented"'),
    (r"\bone\s+platform\s+for\s+all\s+your\b", "one-platform-for-all", '"One platform for all your [noun]"'),
]

# Words that alone are a MEDIUM flag in anti_slop_scan.py; here they escalate
# a template match rather than firing standalone, to avoid duplicate noise
# between the two scripts.
GENERIC_WORDS = (
    "elevate", "seamless", "seamlessly", "unleash", "unlock", "empower",
    "revolutionize", "revolutionary", "cutting-edge", "state-of-the-art",
    "leverage", "robust", "streamline", "frictionless", "effortlessly",
    "supercharge", "next-gen", "next generation", "game-changer",
    "game changing", "all-in-one", "one-stop", "peace of mind",
    "future-proof", "at your fingertips", "take.{0,20}to the next level",
    "transform the way",
)
GENERIC_WORD_RE = re.compile("|".join(GENERIC_WORDS), re.IGNORECASE)

GENERIC_CTAS = {"get started", "learn more", "sign up", "click here", "submit"}

STOPWORDS = {
    "the", "a", "an", "to", "of", "for", "in", "on", "with", "your", "you",
    "and", "or", "is", "it", "that", "this", "one", "no", "not", "into",
    "at", "by",
}


def normalize_words(text: str) -> set[str]:
    words = re.findall(r"[a-z0-9']+", text.lower())
    return {w for w in words if w not in STOPWORDS}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def load_entries(path: Path) -> list[dict]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    return data if isinstance(data, list) else []


def check_templates(label: str, text: str) -> list[str]:
    problems = []
    for pattern, rule, description in TEMPLATE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            problems.append(f"{label} matches template [{rule}]: {description} — text was: \"{text}\"")
    if GENERIC_WORD_RE.search(text):
        hit = GENERIC_WORD_RE.search(text).group(0)
        problems.append(f"{label} contains generic marketing language (\"{hit}\") — swap for a specific, product-true word.")
    return problems


def check_near_duplicate(label: str, text: str, history: list[dict], field: str, window: int, threshold: float) -> list[str]:
    problems = []
    current_words = normalize_words(text)
    for entry in history[:window]:
        past_text = entry.get(field)
        if not past_text:
            continue
        score = jaccard(current_words, normalize_words(past_text))
        if score >= threshold:
            problems.append(
                f"{label} is a near-duplicate ({score:.0%} word overlap) of a recent {field} "
                f"from '{entry.get('project', 'another project')}': \"{past_text}\""
            )
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Check headline/CTA copy for generic templates and cross-project repetition.")
    parser.add_argument("--headline", help="The hero headline text to check.")
    parser.add_argument("--cta", help="The primary CTA label to check.")
    parser.add_argument("--subhead", help="The hero subhead text to check (template check only, not tracked in history).")
    parser.add_argument("--global-log", type=Path, default=DEFAULT_GLOBAL_PATH, help=f"Cross-project copy history (default: {DEFAULT_GLOBAL_PATH})")
    parser.add_argument("--window", type=int, default=10, help="How many recent global entries to compare against (default: 10)")
    parser.add_argument("--threshold", type=float, default=0.6, help="Jaccard word-overlap threshold that counts as a near-duplicate (default: 0.6)")
    args = parser.parse_args()

    if not args.headline and not args.cta and not args.subhead:
        parser.error("pass at least one of --headline, --cta, --subhead")

    problems: list[str] = []
    history = load_entries(args.global_log)

    if args.headline:
        problems.extend(check_templates("Headline", args.headline))
        problems.extend(check_near_duplicate("Headline", args.headline, history, "headline", args.window, args.threshold))
    if args.subhead:
        problems.extend(check_templates("Subhead", args.subhead))
    if args.cta:
        problems.extend(check_templates("CTA", args.cta))
        if args.cta.strip().lower() in GENERIC_CTAS:
            problems.append(f'CTA "{args.cta}" is a generic default — fine only when nothing more specific fits this product\'s first action.')
        problems.extend(check_near_duplicate("CTA", args.cta, history, "cta", args.window, args.threshold))

    if not problems:
        print(f"Copy check passed ({len(history)} global entries checked): reads as specific.")
        return 0

    print("Copy repetition/genericness flagged:")
    for problem in problems:
        print(f"  - {problem}")
    print(
        "\nThis is a nudge, not a hard block. A flagged phrase can still ship if the brief "
        "genuinely earns it — but rewrite first per references/copy-voice.md's three-candidate "
        "method before accepting a flagged line."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
