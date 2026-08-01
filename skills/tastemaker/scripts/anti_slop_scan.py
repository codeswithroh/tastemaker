#!/usr/bin/env python3
"""Scan UI source for high-confidence AI design tells.

This is a static guardrail. It catches patterns that are cheap to detect in
source, then leaves judgment-heavy calls to the anti-slop checklist and browser
review.
"""

from __future__ import annotations

import argparse
import math
import re
from dataclasses import dataclass
from pathlib import Path


EXTENSIONS = {
    ".css",
    ".html",
    ".js",
    ".jsx",
    ".mjs",
    ".ts",
    ".tsx",
    ".vue",
    ".svelte",
}

SKIP_DIRS = {
    ".git",
    ".next",
    ".netlify",
    ".playwright-cli",
    "node_modules",
    "dist",
    "build",
    "coverage",
}

AI_COPY_PHRASES = (
    "elevate",
    "seamless",
    "unleash",
    "next-gen",
    "next generation",
    "game-changer",
    "delve",
    "tapestry",
    "in the world of",
)

PLACEHOLDER_PATTERNS = (
    r"\blorem ipsum\b",
    r"\bjane doe\b",
    r"\bjohn doe\b",
    r"\bacme\b",
    r"\bsample text\b",
)

EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF]",
    re.UNICODE,
)

AI_GRADIENT_HEX_RE = re.compile(
    r"background(?:-image)?\s*:[^;\n}]*(?:linear-gradient|radial-gradient)[^;\n}]*#(?:4f46e5|6366f1|7c3aed|8b5cf6|9333ea|a855f7|06b6d4|22d3ee)",
    re.IGNORECASE,
)

AI_GRADIENT_RGB_RE = re.compile(
    r"background(?:-image)?\s*:[^;\n}]*(?:linear-gradient|radial-gradient)[^;\n}]*rgba?\(\s*(?:99\s*,\s*102\s*,\s*241|124\s*,\s*58\s*,\s*237|139\s*,\s*92\s*,\s*246|147\s*,\s*51\s*,\s*234|168\s*,\s*85\s*,\s*247|6\s*,\s*182\s*,\s*212|34\s*,\s*211\s*,\s*238)",
    re.IGNORECASE,
)


@dataclass
class Finding:
    severity: str
    path: Path
    line: int
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


def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def add_regex(
    findings: list[Finding],
    path: Path,
    text: str,
    pattern: str,
    severity: str,
    rule: str,
    message: str,
    flags: int = re.IGNORECASE,
) -> None:
    for match in re.finditer(pattern, text, flags):
        findings.append(Finding(severity, path, line_number(text, match.start()), rule, message))


def audit_file(path: Path) -> list[Finding]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    findings: list[Finding] = []

    if "tastemaker-scan-ignore-file" in text:
        return findings

    for pattern in (AI_GRADIENT_HEX_RE, AI_GRADIENT_RGB_RE):
        for match in pattern.finditer(text):
            findings.append(
                Finding(
                    "HIGH",
                    path,
                    line_number(text, match.start()),
                    "ai-gradient",
                    "Generic indigo, purple, or cyan gradient detected. Use only when the style lock explicitly earns it.",
                )
            )
    add_regex(
        findings,
        path,
        text,
        r"background-clip\s*:\s*text|bg-clip-text|text-transparent[^\"'\n>]*(?:from-|to-|via-)",
        "HIGH",
        "gradient-text",
        "Gradient text is a default AI tell. Use weight, size, underline, or a locked accent instead.",
    )
    add_regex(
        findings,
        path,
        text,
        r"\bh-screen\b|height\s*:\s*100vh\b",
        "HIGH",
        "viewport-height",
        "Use min-height: 100dvh for full-height sections to avoid mobile browser jumps.",
    )
    add_regex(
        findings,
        path,
        text,
        r"href\s*=\s*[\"']#[\"']",
        "HIGH",
        "dead-link",
        "Dead `href=\"#\"` links make the UI feel unfinished. Link to a real target or disable the control.",
    )
    add_regex(
        findings,
        path,
        text,
        r"<img\b(?:(?!\balt\s*=)[^>])*>",
        "HIGH",
        "missing-alt",
        "Meaningful images need alt text. Decorative images should still declare alt=\"\" explicitly.",
    )
    add_regex(
        findings,
        path,
        text,
        r"transition\s*:\s*all\b|\bclass(?:Name)?\s*=\s*[\"'][^\"']*\btransition-all\b",
        "HIGH",
        "transition-all",
        "Avoid transition-all. Name transform, opacity, color, background, or border-color.",
    )

    for pattern in PLACEHOLDER_PATTERNS:
        add_regex(
            findings,
            path,
            text,
            pattern,
            "HIGH",
            "placeholder-content",
            "Placeholder content shipped in UI source. Replace it with real draft copy or honest sample data.",
        )

    for phrase in AI_COPY_PHRASES:
        add_regex(
            findings,
            path,
            text,
            rf"\b{re.escape(phrase)}\b",
            "MEDIUM",
            "ai-copy",
            f"AI-copy phrase `{phrase}` found. Replace with specific product language.",
        )

    if EMOJI_RE.search(text):
        for match in EMOJI_RE.finditer(text):
            findings.append(
                Finding(
                    "MEDIUM",
                    path,
                    line_number(text, match.start()),
                    "emoji-icon",
                    "Emoji in UI source. Use an icon system unless the brief explicitly asks for social-native emoji.",
                )
            )

    section_count = len(re.findall(r"<section\b|\bclassName\s*=\s*[\"'][^\"']*\bsection\b", text, re.I))
    eyebrow_count = len(
        re.findall(
            r"\bclass(?:Name)?\s*=\s*[\"'][^\"']*(?:\beyebrow\b|\bsection-index\b|uppercase[^\"']{0,80}tracking)",
            text,
            re.I,
        )
    )
    if section_count >= 3 and eyebrow_count > math.ceil(section_count / 3):
        findings.append(
            Finding(
                "MEDIUM",
                path,
                1,
                "eyebrow-spam",
                f"{eyebrow_count} eyebrow-like labels across {section_count} sections. Use at most one per three sections unless the sequence itself matters.",
            )
        )

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit high-confidence AI UI tells.")
    parser.add_argument("paths", nargs="+", type=Path, help="Files or directories to scan")
    parser.add_argument("--max-findings", type=int, default=200)
    parser.add_argument("--fail-on", choices=("high", "medium", "none"), default="high")
    args = parser.parse_args()

    files = iter_files(args.paths)
    findings: list[Finding] = []
    for file_path in files:
        findings.extend(audit_file(file_path))

    if not findings:
        print(f"Anti-slop scan passed: scanned {len(files)} files.")
        return 0

    order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    findings.sort(key=lambda item: (order.get(item.severity, 9), str(item.path), item.line, item.rule))
    for finding in findings[: args.max_findings]:
        print(f"{finding.severity} {finding.path}:{finding.line} [{finding.rule}] {finding.message}")
    if len(findings) > args.max_findings:
        print(f"... {len(findings) - args.max_findings} more finding(s) hidden")

    if args.fail_on == "none":
        return 0
    if args.fail_on == "medium":
        return 1
    return 1 if any(item.severity == "HIGH" for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
